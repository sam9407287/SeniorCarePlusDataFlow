"""扁平化轉換 - 將 4層結構轉換為 2層"""

import apache_beam as beam
import json
import logging
from typing import Any, Dict, Tuple
from datetime import datetime

from ..models.gateway_data import GatewayData, FlattenedGatewayData
from ..models.anchor_data import AnchorData, FlattenedAnchorData


logger = logging.getLogger(__name__)


class FlattenGatewayTransform(beam.DoFn):
    """
    Gateway 扁平化轉換
    
    輸入：4層嵌套的 Gateway 原始數據
    輸出：2層扁平化的 Gateway 數據
    
    Example:
        pipeline | beam.ParDo(FlattenGatewayTransform())
    """
    
    def process(self, element: Dict[str, Any]):
        """
        處理單個 Gateway 記錄
        
        Args:
            element: Gateway JSON 對象或字典
            
        Yields:
            FlattenedGatewayData 的字典表示
        """
        try:
            # 解析輸入
            if isinstance(element, str):
                data = json.loads(element)
            else:
                data = element
            
            # 建立原始 GatewayData 對象
            gateway = GatewayData.from_dict(data)
            
            # 轉換為扁平化格式
            flattened = FlattenedGatewayData.from_gateway_data(gateway)
            
            # 輸出為字典
            yield flattened.to_dict()
            
        except Exception as e:
            logger.error(f"Gateway 轉換失敗: {str(e)}", extra={"element": element})
            # 輸出失敗記錄
            yield {
                "error": True,
                "error_message": str(e),
                "original_data": element,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }


class FlattenAnchorTransform(beam.DoFn):
    """
    Anchor 扁平化轉換
    
    輸入：4層嵌套的 Anchor 原始數據
    輸出：2層扁平化的 Anchor 數據
    
    Example:
        pipeline | beam.ParDo(FlattenAnchorTransform())
    """
    
    def process(self, element: Dict[str, Any]):
        """
        處理單個 Anchor 記錄
        
        Args:
            element: Anchor JSON 對象或字典
            
        Yields:
            FlattenedAnchorData 的字典表示
        """
        try:
            # 解析輸入
            if isinstance(element, str):
                data = json.loads(element)
            else:
                data = element
            
            # 建立原始 AnchorData 對象
            anchor = AnchorData.from_dict(data)
            
            # 轉換為扁平化格式
            flattened = FlattenedAnchorData.from_anchor_data(anchor)
            
            # 輸出為字典
            yield flattened.to_dict()
            
        except Exception as e:
            logger.error(f"Anchor 轉換失敗: {str(e)}", extra={"element": element})
            # 輸出失敗記錄
            yield {
                "error": True,
                "error_message": str(e),
                "original_data": element,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }


class ExtractFieldsTransform(beam.DoFn):
    """
    提取指定字段轉換
    
    用途：從扁平化數據中提取特定字段
    """
    
    def __init__(self, fields: list):
        """
        Args:
            fields: 要提取的字段列表，例如 ["device_id", "battery_voltage"]
        """
        self.fields = fields
    
    def process(self, element: Dict[str, Any]):
        """
        提取指定字段
        
        Args:
            element: 扁平化數據字典
            
        Yields:
            只包含指定字段的字典
        """
        try:
            result = {field: element.get(field) for field in self.fields}
            yield result
        except Exception as e:
            logger.error(f"字段提取失敗: {str(e)}")
            yield {}


class EnrichDataTransform(beam.DoFn):
    """
    數據增強轉換
    
    用途：添加計算字段或外部數據
    """
    
    def process(self, element: Dict[str, Any]):
        """
        增強數據
        
        Args:
            element: 扁平化數據字典
            
        Yields:
            增強後的字典
        """
        try:
            # 複製原始數據
            enriched = element.copy()
            
            # 添加計算字段
            enriched["processing_timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # 信號品質等級
            if "rssi" in enriched and enriched["rssi"] is not None:
                rssi = enriched["rssi"]
                if rssi > -30:
                    enriched["signal_level"] = "excellent"
                elif rssi > -67:
                    enriched["signal_level"] = "good"
                elif rssi > -70:
                    enriched["signal_level"] = "fair"
                else:
                    enriched["signal_level"] = "poor"
            
            # 電池狀態等級
            if "battery_voltage" in enriched and enriched["battery_voltage"] is not None:
                voltage = enriched["battery_voltage"]
                if voltage > 3.5:
                    enriched["battery_level"] = "high"
                elif voltage > 3.0:
                    enriched["battery_level"] = "medium"
                else:
                    enriched["battery_level"] = "low"
            
            yield enriched
            
        except Exception as e:
            logger.error(f"數據增強失敗: {str(e)}")
            yield element




