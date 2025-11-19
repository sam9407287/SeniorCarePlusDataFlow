"""驗證轉換 - 檢查數據完整性和有效性"""

import apache_beam as beam
import logging
from typing import Any, Dict, Tuple
from datetime import datetime


logger = logging.getLogger(__name__)


class ValidateGatewayTransform(beam.DoFn):
    """
    Gateway 數據驗證轉換
    
    檢查：
    - device_id 不為空
    - 必要字段存在
    - 數據類型正確
    """
    
    REQUIRED_FIELDS = ["device_id", "device_type"]
    NUMERIC_FIELDS = ["battery_voltage", "rssi", "position_x", "position_y", "position_z"]
    
    def process(self, element: Dict[str, Any]):
        """
        驗證 Gateway 數據
        
        Args:
            element: Gateway 扁平化數據
            
        Yields:
            (bool, Dict) - (是否有效, 數據)
        """
        errors = []
        
        # 檢查必要字段
        for field in self.REQUIRED_FIELDS:
            if field not in element or not element[field]:
                errors.append(f"缺少必要字段: {field}")
        
        # 檢查數據類型
        for field in self.NUMERIC_FIELDS:
            if field in element and element[field] is not None:
                if not isinstance(element[field], (int, float)):
                    errors.append(f"字段 {field} 類型錯誤: 預期數值型")
        
        # 檢查 RSSI 範圍
        if "rssi" in element and element["rssi"] is not None:
            rssi = element["rssi"]
            if not (-200 < rssi < 0):
                errors.append(f"RSSI 超出範圍: {rssi}")
        
        # 檢查電壓範圍
        if "battery_voltage" in element and element["battery_voltage"] is not None:
            voltage = element["battery_voltage"]
            if not (2.0 < voltage < 5.0):
                errors.append(f"電壓超出範圍: {voltage}")
        
        if errors:
            element["validation_errors"] = errors
            element["is_valid"] = False
            logger.warning(f"Gateway 驗證失敗: {errors}")
        else:
            element["is_valid"] = True
        
        yield element


class ValidateAnchorTransform(beam.DoFn):
    """
    Anchor 數據驗證轉換
    
    檢查：
    - device_id 不為空
    - 必要字段存在
    - 數據類型正確
    - 值域範圍正確
    """
    
    REQUIRED_FIELDS = ["device_id", "device_type"]
    NUMERIC_FIELDS = [
        "battery_voltage", "rssi", "heart_rate", "temperature",
        "position_x", "position_y", "position_z"
    ]
    
    def process(self, element: Dict[str, Any]):
        """
        驗證 Anchor 數據
        
        Args:
            element: Anchor 扁平化數據
            
        Yields:
            驗證後的數據（添加 validation_errors 字段）
        """
        errors = []
        
        # 檢查必要字段
        for field in self.REQUIRED_FIELDS:
            if field not in element or not element[field]:
                errors.append(f"缺少必要字段: {field}")
        
        # 檢查數據類型
        for field in self.NUMERIC_FIELDS:
            if field in element and element[field] is not None:
                if not isinstance(element[field], (int, float)):
                    errors.append(f"字段 {field} 類型錯誤: 預期數值型")
        
        # 檢查心率範圍（正常值：60-100 BPM）
        if "heart_rate" in element and element["heart_rate"] is not None:
            hr = element["heart_rate"]
            if not (30 < hr < 200):  # 允許異常值便於診斷
                logger.warning(f"心率異常: {hr}")
                errors.append(f"心率異常: {hr}")
        
        # 檢查溫度範圍（正常體溫：36-37.5°C）
        if "temperature" in element and element["temperature"] is not None:
            temp = element["temperature"]
            if not (35 < temp < 42):
                logger.warning(f"溫度異常: {temp}")
                errors.append(f"溫度異常: {temp}")
        
        # 檢查 RSSI 範圍
        if "rssi" in element and element["rssi"] is not None:
            rssi = element["rssi"]
            if not (-200 < rssi < 0):
                errors.append(f"RSSI 超出範圍: {rssi}")
        
        # 檢查電壓範圍
        if "battery_voltage" in element and element["battery_voltage"] is not None:
            voltage = element["battery_voltage"]
            if not (2.0 < voltage < 5.0):
                errors.append(f"電壓超出範圍: {voltage}")
        
        if errors:
            element["validation_errors"] = errors
            element["is_valid"] = False
            logger.warning(f"Anchor 驗證失敗: {errors}")
        else:
            element["is_valid"] = True
        
        yield element


class FilterValidRecordsTransform(beam.DoFn):
    """
    過濾有效記錄
    
    輸出格式：(is_valid: bool, record: Dict)
    用於後續的分支處理（有效記錄 vs 無效記錄）
    """
    
    def process(self, element: Dict[str, Any]):
        """
        檢查記錄是否有效
        
        Args:
            element: 包含 is_valid 字段的數據
            
        Yields:
            (bool, Dict) - (是否有效, 完整記錄)
        """
        is_valid = element.get("is_valid", False)
        yield is_valid, element




