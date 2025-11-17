"""Gateway 數據模型 - 4層原始結構和扁平化結構"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, List
from datetime import datetime
import json


@dataclass
class GatewayData:
    """
    Gateway 原始 4層結構
    
    Example:
    {
        "gateway_id": "gw_123",
        "name": "Living Room Gateway",
        "ip_address": "192.168.1.100",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "cloudData": {
            "id": 1,
            "gateway_id": 1,
            "pub": {
                "msg": {
                    "data": {
                        "battery_voltage": 3.7,
                        "rssi": -45,
                        "status": "online"
                    }
                }
            },
            "config": {...},
            "fw_version": "v2.1.0"
        },
        "position": {"x": 10.5, "y": 20.3, "z": 1.2},
        "createdAt": "2025-11-17T10:00:00Z",
        "lastSeen": "2025-11-17T14:30:00Z"
    }
    """
    
    gateway_id: str
    name: str
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    cloud_data: Optional[Dict[str, Any]] = None
    position: Optional[Dict[str, float]] = None
    created_at: Optional[str] = None
    last_seen: Optional[str] = None
    status: str = "unknown"
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
    def from_dict(cls, data: Dict[str, Any]) -> "GatewayData":
        """從字典建立實例"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "GatewayData":
        """從 JSON 字符串建立實例"""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class FlattenedGatewayData:
    """
    Gateway 扁平化結構（2層）
    
    第1層：設備基本信息
    第2層：事件數據/配置數據
    
    Example:
    {
        # 第1層：設備基本信息
        "device_id": "gw_123",
        "device_type": "gateway",
        "device_name": "Living Room Gateway",
        "ip_address": "192.168.1.100",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "position_x": 10.5,
        "position_y": 20.3,
        "position_z": 1.2,
        "status": "online",
        "created_at": "2025-11-17T10:00:00Z",
        "last_seen": "2025-11-17T14:30:00Z",
        
        # 第2層：事件數據（從 cloudData.pub.msg.data 提取）
        "battery_voltage": 3.7,
        "rssi": -45,
        "signal_quality": "strong",
        "fw_version": "v2.1.0",
        "config_mode": "auto",
        
        # 中繼數據
        "is_bound": False,
        "timestamp": "2025-11-17T14:35:00Z",
        "processing_timestamp": "2025-11-17T14:35:10Z"
    }
    """
    
    # 第1層：設備基本信息
    device_id: str
    device_type: str = "gateway"
    device_name: str = ""
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    
    # 位置信息
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    position_z: Optional[float] = None
    
    # 設備狀態
    status: str = "unknown"
    created_at: Optional[str] = None
    last_seen: Optional[str] = None
    
    # 第2層：事件數據
    battery_voltage: Optional[float] = None
    rssi: Optional[int] = None
    signal_quality: Optional[str] = None
    fw_version: Optional[str] = None
    config_mode: Optional[str] = None
    
    # 中繼數據
    is_bound: bool = False
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
    def from_dict(cls, data: Dict[str, Any]) -> "FlattenedGatewayData":
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
    def from_json(cls, json_str: str) -> "FlattenedGatewayData":
        """從 JSON 字符串建立實例"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_gateway_data(cls, gateway: GatewayData) -> "FlattenedGatewayData":
        """從原始 GatewayData 轉換"""
        # 提取 cloudData 中的數據
        battery_voltage = None
        rssi = None
        signal_quality = None
        fw_version = None
        config_mode = None
        
        if gateway.cloud_data:
            # 深層提取：cloudData -> pub -> msg -> data
            cloud_data = gateway.cloud_data
            if isinstance(cloud_data, dict):
                battery_voltage = cloud_data.get("battery_voltage")
                rssi = cloud_data.get("rssi")
                signal_quality = cloud_data.get("signal_quality")
                fw_version = cloud_data.get("fw_version")
                config_mode = cloud_data.get("config_mode")
                
                # 嘗試從 pub -> msg -> data 提取
                pub = cloud_data.get("pub")
                if pub and isinstance(pub, dict):
                    msg = pub.get("msg")
                    if msg and isinstance(msg, dict):
                        data = msg.get("data")
                        if data and isinstance(data, dict):
                            battery_voltage = battery_voltage or data.get("battery_voltage")
                            rssi = rssi or data.get("rssi")
                            signal_quality = signal_quality or data.get("signal_quality")
        
        # 提取位置信息
        position_x, position_y, position_z = None, None, None
        if gateway.position and isinstance(gateway.position, dict):
            position_x = gateway.position.get("x")
            position_y = gateway.position.get("y")
            position_z = gateway.position.get("z")
        
        return cls(
            device_id=gateway.gateway_id,
            device_type="gateway",
            device_name=gateway.name,
            ip_address=gateway.ip_address,
            mac_address=gateway.mac_address,
            position_x=position_x,
            position_y=position_y,
            position_z=position_z,
            status=gateway.status,
            created_at=gateway.created_at,
            last_seen=gateway.last_seen,
            battery_voltage=battery_voltage,
            rssi=rssi,
            signal_quality=signal_quality,
            fw_version=fw_version,
            config_mode=config_mode,
            is_bound=gateway.is_bound,
            processing_timestamp=datetime.utcnow().isoformat() + "Z",
            timestamp=gateway.last_seen
        )

