"""Gateway 扁平化 Pipeline"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import logging
import json
from typing import Dict, Any

from ..transforms.flatten_transform import FlattenGatewayTransform, EnrichDataTransform
from ..transforms.validation_transform import ValidateGatewayTransform, FilterValidRecordsTransform


logger = logging.getLogger(__name__)


class GatewayFlatteningPipeline:
    """
    Gateway 數據扁平化 Pipeline
    
    Flow:
    1. 讀取原始 4層 Gateway 數據 (Pub/Sub 或文件)
    2. 驗證數據完整性
    3. 扁平化為 2層結構
    4. 數據增強（添加計算字段）
    5. 分支輸出：
       - 有效數據 → BigQuery + Redis
       - 無效數據 → 錯誤日誌表
    
    Example:
        pipeline = GatewayFlatteningPipeline()
        pipeline.run(
            runner="DirectRunner",
            input_type="file",
            input_path="test_data/gateways.json"
        )
    """
    
    def __init__(self, project_id: str = None, region: str = "asia-east1"):
        """
        初始化 Pipeline
        
        Args:
            project_id: GCP 項目 ID
            region: GCP 區域
        """
        self.project_id = project_id
        self.region = region
    
    def run(self,
            runner: str = "DirectRunner",
            input_type: str = "file",
            input_path: str = None,
            input_topic: str = None,
            output_bigquery: str = None,
            output_file: str = None):
        """
        執行 Pipeline
        
        Args:
            runner: "DirectRunner" (本地) 或 "DataflowRunner" (GCP)
            input_type: "file" 或 "pubsub"
            input_path: 輸入文件路徑 (file 模式)
            input_topic: Pub/Sub 主題 (pubsub 模式)
            output_bigquery: BigQuery 表 (格式：project:dataset.table)
            output_file: 輸出文件 (用於測試)
        """
        
        # 建立 Pipeline Options
        options = PipelineOptions()
        options.view_as(StandardOptions).runner = runner
        
        if runner == "DataflowRunner":
            options.view_as(StandardOptions).project = self.project_id
            options.view_as(StandardOptions).region = self.region
        
        # 建立 Pipeline
        with beam.Pipeline(options=options) as pipeline:
            # 讀取輸入
            if input_type == "file":
                raw_data = (
                    pipeline
                    | f"讀取文件" >> beam.io.ReadFromText(input_path)
                    | "解析 JSON" >> beam.Map(lambda x: json.loads(x))
                )
            elif input_type == "pubsub":
                raw_data = (
                    pipeline
                    | f"讀取 Pub/Sub" >> beam.io.gcp.pubsub.ReadFromPubSub(topic=input_topic)
                    | "解析 JSON" >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
                )
            else:
                raise ValueError(f"未支持的輸入類型: {input_type}")
            
            # Step 1: 驗證數據
            validated = (
                raw_data
                | "驗證 Gateway" >> beam.ParDo(ValidateGatewayTransform())
            )
            
            # Step 2: 扁平化
            flattened = (
                validated
                | "扁平化 Gateway" >> beam.ParDo(FlattenGatewayTransform())
            )
            
            # Step 3: 數據增強
            enriched = (
                flattened
                | "數據增強" >> beam.ParDo(EnrichDataTransform())
            )
            
            # Step 4: 過濾有效記錄
            valid_records, invalid_records = (
                enriched
                | "分類有效性" >> beam.ParDo(FilterValidRecordsTransform())
                | "分支" >> beam.Partition(
                    lambda element, num_partitions: 0 if element[0] else 1,
                    2
                )
            )
            
            # 解開元組
            valid_only = valid_records | "提取有效" >> beam.Map(lambda x: x[1])
            invalid_only = invalid_records | "提取無效" >> beam.Map(lambda x: x[1])
            
            # Step 5a: 有效數據輸出
            if output_bigquery:
                (
                    valid_only
                    | "轉換為 BigQuery 行" >> beam.Map(self._to_bigquery_row)
                    | "寫入 BigQuery" >> beam.io.gcp.bigquery.WriteToBigQuery(
                        table=output_bigquery,
                        create_disposition=beam.io.gcp.bigquery.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.gcp.bigquery.BigQueryDisposition.WRITE_APPEND
                    )
                )
            
            if output_file:
                (
                    valid_only
                    | "序列化" >> beam.Map(json.dumps)
                    | "寫入文件" >> beam.io.WriteToText(output_file)
                )
            
            # Step 5b: 無效數據記錄
            (
                invalid_only
                | "記錄無效" >> beam.Map(lambda x: f"Invalid: {json.dumps(x)}")
                | "寫入錯誤日誌" >> beam.io.WriteToText("/tmp/gateway_errors")
            )
    
    @staticmethod
    def _to_bigquery_row(element: Dict[str, Any]) -> Dict[str, Any]:
        """
        轉換為 BigQuery 行
        
        BigQuery 要求所有字段都有值（None -> null）
        """
        return {
            k: v for k, v in element.items()
            if v is not None
        }


def run_local_test():
    """本地測試"""
    pipeline = GatewayFlatteningPipeline()
    pipeline.run(
        runner="DirectRunner",
        input_type="file",
        input_path="test_data/gateways.json",
        output_file="/tmp/gateway_flattened"
    )
    print("✅ Gateway 扁平化完成")
    print("輸出位置: /tmp/gateway_flattened*")


if __name__ == "__main__":
    run_local_test()




