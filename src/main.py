"""
Main entry point for DataFlow Pipeline
"""

import argparse
import sys
import logging

from src.pipelines.gateway_flattening import GatewayFlatteningPipeline
from src.pipelines.anchor_flattening import AnchorFlatteningPipeline
from src.config import get_config
from src.utils import setup_logger


def main():
    """主程序入口"""
    
    parser = argparse.ArgumentParser(
        description="Senior Care Plus DataFlow Pipeline"
    )
    
    # 基本參數
    parser.add_argument(
        "--runner",
        choices=["DirectRunner", "DataflowRunner"],
        default="DirectRunner",
        help="Pipeline 執行器 (default: DirectRunner)"
    )
    
    parser.add_argument(
        "--env",
        choices=["dev", "test", "prod"],
        default="dev",
        help="環境配置 (default: dev)"
    )
    
    parser.add_argument(
        "--pipeline",
        choices=["gateway", "anchor", "both"],
        default="gateway",
        help="要執行的 Pipeline (default: gateway)"
    )
    
    # 輸入參數
    parser.add_argument(
        "--input-type",
        choices=["file", "pubsub"],
        default="file",
        help="輸入類型 (default: file)"
    )
    
    parser.add_argument(
        "--input-file",
        help="輸入文件路徑 (file 模式)"
    )
    
    parser.add_argument(
        "--input-topic",
        help="Pub/Sub 主題 (pubsub 模式)"
    )
    
    # 輸出參數
    parser.add_argument(
        "--output-file",
        help="輸出文件路徑 (用於測試)"
    )
    
    parser.add_argument(
        "--output-bigquery",
        help="BigQuery 輸出表 (格式: project:dataset.table)"
    )
    
    # 日誌參數
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="日誌級別 (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # 設置日誌
    logger = setup_logger("dataflow", args.log_level)
    logger.info(f"啟動 DataFlow Pipeline (環境: {args.env})")
    
    # 讀取配置
    config = get_config(args.env)
    logger.info(f"項目: {config.project_id}, 區域: {config.region}")
    
    # 驗證輸入
    if args.input_type == "file" and not args.input_file:
        logger.error("--input-file 參數必須提供")
        sys.exit(1)
    
    if args.input_type == "pubsub" and not args.input_topic:
        logger.error("--input-topic 參數必須提供")
        sys.exit(1)
    
    # 執行 Pipeline
    try:
        if args.pipeline in ["gateway", "both"]:
            logger.info("執行 Gateway 扁平化 Pipeline...")
            gateway_pipeline = GatewayFlatteningPipeline(
                project_id=config.project_id,
                region=config.region
            )
            gateway_pipeline.run(
                runner=args.runner,
                input_type=args.input_type,
                input_path=args.input_file,
                input_topic=args.input_topic,
                output_bigquery=args.output_bigquery,
                output_file=args.output_file
            )
            logger.info("✅ Gateway Pipeline 完成")
        
        if args.pipeline in ["anchor", "both"]:
            logger.info("執行 Anchor 扁平化 Pipeline...")
            anchor_pipeline = AnchorFlatteningPipeline(
                project_id=config.project_id,
                region=config.region
            )
            anchor_pipeline.run(
                runner=args.runner,
                input_type=args.input_type,
                input_path=args.input_file,
                input_topic=args.input_topic,
                output_bigquery=args.output_bigquery,
                output_file=args.output_file
            )
            logger.info("✅ Anchor Pipeline 完成")
        
        logger.info("🎉 所有 Pipeline 執行完成")
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline 執行失敗: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

