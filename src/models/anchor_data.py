"""Anchor 數據模型 - 4層原始結構和扁平化結構"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional
from datetime import datetime
import json


@dataclass
class AnchorData:
    """
    Anchor 原始 4層結構
    
    Example:
    {
        "anchor_id": "anchor_001",
        "gateway_id": "gw_123",
        "name": "Bed Anchor",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "cloudData": {
            "id": 1,
            "gateway_id": 1,
            "name": "Bed Anchor",
            "node": "node_1",
            "content": "anchor",
            "pub": {
                "msg": {
                    "data": {
                        "battery_voltage": 3.2,
                        "rssi": -52,
                        "heart_rate": 72,
                        "temperature": 36.5
                    }
                }
            },
            "fw_update": 0,
            "led": 1,
            "ble": 1,
            "initiator": 0,
            "position": {"x": 5.2, "y": 8.1, "z": 0.8},
            "receivedAt": "2025-11-17T14:30:00Z"
        },
        "position": {"x": 5.2, "y": 8.1, "z": 0.8},
        "status": "online",
        "lastSeen": "2025-11-17T14:35:00Z",
        "isBound": true
    }
    """
    
    anchor_id: str
    gateway_id: Optional[str] = None
    name: str = ""
    mac_address: Optional[str] = None
    cloud_data: Optional[Dict[str, Any]] = None
    position: Optional[Dict[str, float]] = None
    status: str = "unknown"
    last_seen: Optional[str] = None
    is_bound: bool = False
    
    # 其他自訂字段
    extra_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return asdict(self)
    
    def to_json(self) -> str:
        """轉換為 JSON 字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnchorData":
        """從字典建立實例"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "AnchorData":
        """從 JSON 字符串建立實例"""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class FlattenedAnchorData:
    """
    Anchor 扁平化結構（2層）
    
    第1層：設備基本信息
    第2層：傳感器數據
    
    Example:
    {
        # 第1層：設備基本信息
        "device_id": "anchor_001",
        "device_type": "anchor",
        "device_name": "Bed Anchor",
        "gateway_id": "gw_123",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "position_x": 5.2,
        "position_y": 8.1,
        "position_z": 0.8,
        "status": "online",
        "last_seen": "2025-11-17T14:35:00Z",
        "is_bound": true,
        
        # 第2層：傳感器數據
        "battery_voltage": 3.2,
        "rssi": -52,
        "heart_rate": 72,
        "temperature": 36.5,
        "fw_update": false,
        "led_enabled": true,
        "ble_enabled": true,
        "is_initiator": false,
        
        # 中繼數據
        "timestamp": "2025-11-17T14:35:00Z",
        "processing_timestamp": "2025-11-17T14:35:10Z"
    }
    """
    
    # 第1層：設備基本信息
    device_id: str
    device_type: str = "anchor"
    device_name: str = ""
    gateway_id: Optional[str] = None
    mac_address: Optional[str] = None
    
    # 位置信息
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    position_z: Optional[float] = None
    
    # 設備狀態
    status: str = "unknown"
    last_seen: Optional[str] = None
    is_bound: bool = False
    
    # 第2層：傳感器數據
    battery_voltage: Optional[float] = None
    rssi: Optional[int] = None
    heart_rate: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    
    # 設備配置
    fw_update: Optional[bool] = None
    led_enabled: Optional[bool] = None
    ble_enabled: Optional[bool] = None
    is_initiator: Optional[bool] = None
    
    # 中繼數據
    timestamp: Optional[str] = None
    processing_timestamp: Optional[str] = None
    
    # 其他自訂字段
    extra_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典（排除 None 值）"""
        return {
            k: v for k, v in asdict(self).items()
            if v is not None and k != "extra_data"
        } | self.extra_data
    
    def to_json(self) -> str:
        """轉換為 JSON 字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FlattenedAnchorData":
        """從字典建立實例"""
        # 提取已知字段
        kwargs = {}
        for field_name in cls.__dataclass_fields__:
            if field_name in data:
                kwargs[field_name] = data[field_name]
        
        # 其他字段放到 extra_data
        extra = {k: v for k, v in data.items() if k not in kwargs}
        kwargs["extra_data"] = extra
        
        return cls(**kwargs)
    
    @classmethod
    def from_json(cls, json_str: str) -> "FlattenedAnchorData":
        """從 JSON 字符串建立實例"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_anchor_data(cls, anchor: AnchorData) -> "FlattenedAnchorData":
        """從原始 AnchorData 轉換"""
        # 提取 cloudData 中的數據
        battery_voltage = None
        rssi = None
        heart_rate = None
        temperature = None
        humidity = None
        fw_update = None
        led_enabled = None
        ble_enabled = None
        is_initiator = None
        
        if anchor.cloud_data:
            cloud_data = anchor.cloud_data
            if isinstance(cloud_data, dict):
                battery_voltage = cloud_data.get("battery_voltage")
                rssi = cloud_data.get("rssi")
                heart_rate = cloud_data.get("heart_rate")
                temperature = cloud_data.get("temperature")
                humidity = cloud_data.get("humidity")
                fw_update = cloud_data.get("fw_update")
                led_enabled = cloud_data.get("led")
                ble_enabled = cloud_data.get("ble")
                is_initiator = cloud_data.get("initiator")
                
                # 嘗試從 pub -> msg -> data 提取
                pub = cloud_data.get("pub")
                if pub and isinstance(pub, dict):
                    msg = pub.get("msg")
                    if msg and isinstance(msg, dict):
                        data = msg.get("data")
                        if data and isinstance(data, dict):
                            battery_voltage = battery_voltage or data.get("battery_voltage")
                            rssi = rssi or data.get("rssi")
                            heart_rate = heart_rate or data.get("heart_rate")
                            temperature = temperature or data.get("temperature")
                            humidity = humidity or data.get("humidity")
        
        # 轉換布林值（0/1 -> False/True）
        if isinstance(fw_update, int):
            fw_update = bool(fw_update)
        if isinstance(led_enabled, int):
            led_enabled = bool(led_enabled)
        if isinstance(ble_enabled, int):
            ble_enabled = bool(ble_enabled)
        if isinstance(is_initiator, int):
            is_initiator = bool(is_initiator)
        
        # 提取位置信息
        position_x, position_y, position_z = None, None, None
        if anchor.position and isinstance(anchor.position, dict):
            position_x = anchor.position.get("x")
            position_y = anchor.position.get("y")
            position_z = anchor.position.get("z")
        elif anchor.cloud_data and isinstance(anchor.cloud_data, dict):
            pos = anchor.cloud_data.get("position")
            if pos and isinstance(pos, dict):
                position_x = pos.get("x")
                position_y = pos.get("y")
                position_z = pos.get("z")
        
        return cls(
            device_id=anchor.anchor_id,
            device_type="anchor",
            device_name=anchor.name,
            gateway_id=anchor.gateway_id,
            mac_address=anchor.mac_address,
            position_x=position_x,
            position_y=position_y,
            position_z=position_z,
            status=anchor.status,
            last_seen=anchor.last_seen,
            is_bound=anchor.is_bound,
            battery_voltage=battery_voltage,
            rssi=rssi,
            heart_rate=heart_rate,
            temperature=temperature,
            humidity=humidity,
            fw_update=fw_update,
            led_enabled=led_enabled,
            ble_enabled=ble_enabled,
            is_initiator=is_initiator,
            processing_timestamp=datetime.utcnow().isoformat() + "Z",
            timestamp=anchor.last_seen
        )




