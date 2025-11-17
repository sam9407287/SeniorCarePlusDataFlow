"""轉換測試"""

import unittest
import json
from src.models.gateway_data import GatewayData, FlattenedGatewayData
from src.models.anchor_data import AnchorData, FlattenedAnchorData
from src.transforms.flatten_transform import FlattenGatewayTransform, FlattenAnchorTransform


class TestGatewayFlattening(unittest.TestCase):
    """Gateway 扁平化轉換測試"""
    
    def setUp(self):
        """測試前置"""
        self.sample_gateway = {
            "gateway_id": "gw_001",
            "name": "Living Room",
            "ip_address": "192.168.1.100",
            "mac_address": "00:1A:2B:3C:4D:5E",
            "cloudData": {
                "id": 1,
                "gateway_id": 1,
                "pub": {
                    "msg": {
                        "data": {
                            "battery_voltage": 3.7,
                            "rssi": -45
                        }
                    }
                },
                "fw_version": "v2.1.0"
            },
            "position": {"x": 10.5, "y": 20.3, "z": 1.2},
            "status": "online",
            "lastSeen": "2025-11-17T14:30:00Z"
        }
    
    def test_gateway_data_creation(self):
        """測試 GatewayData 對象創建"""
        gateway = GatewayData.from_dict(self.sample_gateway)
        self.assertEqual(gateway.gateway_id, "gw_001")
        self.assertEqual(gateway.name, "Living Room")
        self.assertEqual(gateway.status, "online")
    
    def test_gateway_flattening(self):
        """測試 Gateway 扁平化"""
        gateway = GatewayData.from_dict(self.sample_gateway)
        flattened = FlattenedGatewayData.from_gateway_data(gateway)
        
        # 檢查第1層
        self.assertEqual(flattened.device_id, "gw_001")
        self.assertEqual(flattened.device_type, "gateway")
        self.assertEqual(flattened.device_name, "Living Room")
        
        # 檢查位置
        self.assertEqual(flattened.position_x, 10.5)
        self.assertEqual(flattened.position_y, 20.3)
        self.assertEqual(flattened.position_z, 1.2)
        
        # 檢查第2層（從 cloudData 提取）
        self.assertEqual(flattened.battery_voltage, 3.7)
        self.assertEqual(flattened.rssi, -45)
        self.assertEqual(flattened.fw_version, "v2.1.0")
    
    def test_gateway_to_dict(self):
        """測試 Gateway 轉換為字典"""
        gateway = GatewayData.from_dict(self.sample_gateway)
        flattened = FlattenedGatewayData.from_gateway_data(gateway)
        
        result = flattened.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn("device_id", result)
        self.assertIn("battery_voltage", result)
    
    def test_gateway_to_json(self):
        """測試 Gateway 轉換為 JSON"""
        gateway = GatewayData.from_dict(self.sample_gateway)
        flattened = FlattenedGatewayData.from_gateway_data(gateway)
        
        json_str = flattened.to_json()
        self.assertIsInstance(json_str, str)
        
        # 驗證可以解析回去
        parsed = json.loads(json_str)
        self.assertEqual(parsed["device_id"], "gw_001")


class TestAnchorFlattening(unittest.TestCase):
    """Anchor 扁平化轉換測試"""
    
    def setUp(self):
        """測試前置"""
        self.sample_anchor = {
            "anchor_id": "anchor_001",
            "gateway_id": "gw_001",
            "name": "Bed Anchor",
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "cloudData": {
                "id": 1,
                "gateway_id": 1,
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
                "position": {"x": 5.2, "y": 8.1, "z": 0.8}
            },
            "position": {"x": 5.2, "y": 8.1, "z": 0.8},
            "status": "online",
            "lastSeen": "2025-11-17T14:30:00Z",
            "isBound": True
        }
    
    def test_anchor_data_creation(self):
        """測試 AnchorData 對象創建"""
        anchor = AnchorData.from_dict(self.sample_anchor)
        self.assertEqual(anchor.anchor_id, "anchor_001")
        self.assertEqual(anchor.name, "Bed Anchor")
        self.assertEqual(anchor.is_bound, True)
    
    def test_anchor_flattening(self):
        """測試 Anchor 扁平化"""
        anchor = AnchorData.from_dict(self.sample_anchor)
        flattened = FlattenedAnchorData.from_anchor_data(anchor)
        
        # 檢查第1層
        self.assertEqual(flattened.device_id, "anchor_001")
        self.assertEqual(flattened.device_type, "anchor")
        self.assertEqual(flattened.device_name, "Bed Anchor")
        
        # 檢查位置
        self.assertEqual(flattened.position_x, 5.2)
        self.assertEqual(flattened.position_y, 8.1)
        self.assertEqual(flattened.position_z, 0.8)
        
        # 檢查第2層（從 cloudData 提取）
        self.assertEqual(flattened.battery_voltage, 3.2)
        self.assertEqual(flattened.rssi, -52)
        self.assertEqual(flattened.heart_rate, 72)
        self.assertEqual(flattened.temperature, 36.5)
        
        # 檢查布林轉換
        self.assertEqual(flattened.fw_update, False)
        self.assertEqual(flattened.led_enabled, True)
        self.assertEqual(flattened.ble_enabled, True)
        self.assertEqual(flattened.is_initiator, False)
    
    def test_anchor_to_dict(self):
        """測試 Anchor 轉換為字典"""
        anchor = AnchorData.from_dict(self.sample_anchor)
        flattened = FlattenedAnchorData.from_anchor_data(anchor)
        
        result = flattened.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn("device_id", result)
        self.assertIn("heart_rate", result)


if __name__ == "__main__":
    unittest.main()

