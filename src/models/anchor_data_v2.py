"""Anchor 數據模型 v2 - 保留 2層結構，超過 2層的才拆解並加前綴"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional
from datetime import datetime
import json


@dataclass
class FlattenedAnchorDataV2:
    """
    Anchor 扁平化結構 v2（2層結構）
    
    設計原則：
    1. 原始 ≤ 2層的結構保留不動
    2. 原始 > 2層的結構拆到最內 2層，加上「路徑前綴」
    3. 最終結構是 2層：第1層根字段 + 第2層帶前綴的巢狀字段
    
    Example:
    {
        # 第1層：根層字段（保持不變）
        "anchor_id": "anchor_001",
        "gateway_id": "gw_001",
        "name": "DW30C5",
        "mac_address": "ANCHOR:12485",
        "status": "active",
        "position": {"x": 59.65, "y": -69.24, "z": 1},
        "last_seen": "2025-11-11T15:58:05.295Z",
        "is_bound": true,
        
        # 第2層：cloud_data 物件（保留物件結構，加前綴區分）
        "cloud_data": {
            "gateway_id": 4192812156,           ← 區分於根層的 gateway_id
            "node": "ANCHOR",
            "name": "DW30C5",
            "id": 12485,
            "fw_update": 0,
            "led": 1,
            "ble": 1,
            "initiator": 1,
            "position": {"x": -150.64, "y": 1.33, "z": 1},  ← 區分於根層的 position
            "content": "config",
            "receivedAt": "2025-11-11T15:58:05.295Z",
            "pub": {
                "msg": {
                    "data": {
                        "battery_voltage": 3.2,
                        "rssi": -52
                    }
                }
            }
        },
        
        # 中繼數據
        "device_type": "anchor",
        "device_id": "anchor_1762876688408",
        "device_name": "DW30C5",
        "timestamp": "2025-11-11T15:58:05.295Z",
        "processing_timestamp": "2025-11-19T01:06:19.350531Z"
    }
    """
    
    # 第1層：根層字段
    anchor_id: str
    gateway_id: Optional[str] = None
    name: str = ""
    mac_address: Optional[str] = None
    status: str = "unknown"
    position: Optional[Dict[str, Any]] = None
    last_seen: Optional[str] = None
    is_bound: bool = False
    
    # 第2層：cloud_data 物件（保留物件結構）
    cloud_data: Optional[Dict[str, Any]] = None
    
    # 中繼數據
    device_type: str = "anchor"
    device_id: Optional[str] = None
    device_name: Optional[str] = None
    timestamp: Optional[str] = None
    processing_timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典（保留 2層結構）"""
        result = {
            "anchor_id": self.anchor_id,
            "gateway_id": self.gateway_id,
            "name": self.name,
            "mac_address": self.mac_address,
            "status": self.status,
            "last_seen": self.last_seen,
            "is_bound": self.is_bound,
            "device_type": self.device_type,
            "device_id": self.device_id,
            "device_name": self.device_name,
            "timestamp": self.timestamp,
            "processing_timestamp": self.processing_timestamp,
        }
        
        # 保留 position 物件
        if self.position:
            result["position"] = self.position
        
        # 保留 cloud_data 物件（完整保留，不展開）
        if self.cloud_data:
            result["cloud_data"] = self.cloud_data
        
        return result
    
    def to_json(self) -> str:
        """轉換為 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FlattenedAnchorDataV2":
        """從字典建立實例"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "FlattenedAnchorDataV2":
        """從 JSON 字符串建立實例"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_anchor_data(cls, raw_data: Dict[str, Any]) -> "FlattenedAnchorDataV2":
        """
        從原始 Anchor 數據轉換
        
        轉換邏輯：
        1. 第1層字段直接保留
        2. ≤2層的物件結構保留不動
        3. >2層的結構拆到最內 2層，保留 cloud_data 物件
        4. 提升深層數據到 cloud_data 物件內（保留 cloud_data 容器）
        """
        
        # 第1層字段
        anchor_id = raw_data.get("anchor_id", "")
        gateway_id = raw_data.get("gateway_id")
        name = raw_data.get("name", "")
        mac_address = raw_data.get("mac_address")
        status = raw_data.get("status", "unknown")
        last_seen = raw_data.get("last_seen")
        is_bound = raw_data.get("is_bound", False)
        
        # 第1層：position 物件（保留不動）
        position = raw_data.get("position")
        
        # 第2層：cloud_data 物件（處理深層數據）
        cloud_data_input = raw_data.get("cloud_data", {})
        cloud_data_output = {}
        
        if cloud_data_input and isinstance(cloud_data_input, dict):
            # 複製所有字段
            for key, value in cloud_data_input.items():
                if key == "pub" and isinstance(value, dict):
                    # 處理深層 pub.msg.data，提升字段到 cloud_data 層級
                    pub_obj = value
                    msg_obj = pub_obj.get("msg", {})
                    data_obj = msg_obj.get("data", {})
                    
                    # 將 data 層級的字段提升到 cloud_data，加上路徑前綴
                    if isinstance(data_obj, dict):
                        for data_key, data_value in data_obj.items():
                            prefixed_key = f"pub.msg.data.{data_key}"
                            cloud_data_output[prefixed_key] = data_value
                    
                    # 也保留 pub 的完整物件結構
                    cloud_data_output["pub"] = value
                else:
                    # 其他字段直接保留
                    cloud_data_output[key] = value
        
        return cls(
            anchor_id=anchor_id,
            gateway_id=gateway_id,
            name=name,
            mac_address=mac_address,
            status=status,
            position=position,
            last_seen=last_seen,
            is_bound=is_bound,
            cloud_data=cloud_data_output if cloud_data_output else None,
            device_type="anchor",
            device_id=raw_data.get("anchor_id"),
            device_name=raw_data.get("name"),
            timestamp=raw_data.get("last_seen"),
            processing_timestamp=datetime.utcnow().isoformat() + "Z"
        )

