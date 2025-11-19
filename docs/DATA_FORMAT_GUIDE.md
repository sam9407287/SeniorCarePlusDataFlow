# 📊 數據格式完整指南

> 本指南適合所有開發者：**後端理解設計，前端快速開發**

## 📖 目錄

- [🎯 快速參考](#快速參考)
- [🏗️ 架構概述](#架構概述)
- [🔌 Gateway 數據格式](#gateway-數據格式)
- [🔌 Anchor 數據格式](#anchor-數據格式)
- [📤 前端發送的格式](#前端發送的格式)
- [💾 存儲層格式](#存儲層格式)
- [📝 使用示例](#使用示例)

---

## 🎯 快速參考

### Gateway vs Anchor 對比表

| 特性 | Gateway | Anchor |
|------|---------|--------|
| **用途** | 無線網關/基站 | 穿戴式標籤/傳感器 |
| **包含的信息** | 設備狀態、網絡狀況 | 生理數據、位置信息 |
| **關鍵字段** | ip_address, battery_voltage, rssi | heart_rate, temperature, position |
| **發送頻率** | 5 秒/次 | 5 秒/次 |
| **綁定** | 綁定到 Floor | 綁定到 Gateway |

### 字段速查表

| 字段名 | Gateway | Anchor | 類型 | 說明 |
|--------|---------|--------|------|------|
| device_id | ✅ | ✅ | string | 設備唯一 ID |
| device_type | ✅ | ✅ | string | "gateway" 或 "anchor" |
| device_name | ✅ | ✅ | string | 人易讀名稱 |
| gateway_id | ❌ | ✅ | string | 所屬 Gateway ID |
| ip_address | ✅ | ❌ | string | 網關 IP 地址 |
| battery_voltage | ✅ | ✅ | number | 電池電壓（V） |
| rssi | ✅ | ✅ | number | 信號強度（dBm） |
| heart_rate | ❌ | ✅ | number | 心率（bpm） |
| temperature | ❌ | ✅ | number | 體溫（°C） |
| position_x, y, z | ✅ | ✅ | number | 3D 位置坐標 |
| timestamp | ✅ | ✅ | string | ISO 8601 時戳 |
| status | ✅ | ✅ | string | "online" 或 "offline" |
| is_bound | ✅ | ✅ | boolean | 是否已綁定 |

---

## 🏗️ 架構概述

### 數據轉換流程

```
原始 MQTT 消息 (4層嵌套)
      ↓
Cloud Pub/Sub
      ↓
Cloud Dataflow Pipeline
  ├─ 驗證
  ├─ 去重
  ├─ 扁平化 (4層 → 2層)
  ├─ 增強
  └─ 分類
      ↓
FlattenedGatewayData / FlattenedAnchorData (2層扁平結構)
      ↓
┌─────────────────────────────────────┐
│ 存儲位置                              │
├─────────────────────────────────────┤
│ Redis (熱層): 最新 1 小時             │
│ BigQuery (冷層): 30 天歷史            │
│ PostgreSQL (靜態): 元數據配置         │
└─────────────────────────────────────┘
```

### 數據層級定義

**第1層：設備基本信息**
- 設備的標識和配置（變動不頻繁）
- 例：device_id, device_name, ip_address, status

**第2層：事件數據**
- 傳感器讀數和設備狀態（高頻變動）
- 例：battery_voltage, rssi, heart_rate, temperature

---

## 🔌 Gateway 數據格式

### 完整字段列表

```json
{
  "device_id": "gw_001",
  "device_type": "gateway",
  "device_name": "客廳網關",
  "ip_address": "192.168.1.100",
  "mac_address": "00:1A:2B:3C:4D:5E",
  
  "position_x": 10.5,
  "position_y": 20.3,
  "position_z": 1.2,
  
  "status": "online",
  "battery_voltage": 3.7,
  "rssi": -45,
  "signal_quality": "strong",
  
  "fw_version": "v2.1.0",
  "config_mode": "auto",
  
  "is_bound": true,
  "created_at": "2025-11-17T10:00:00Z",
  "last_seen": "2025-11-17T14:30:00Z",
  "timestamp": "2025-11-17T14:30:00Z",
  "processing_timestamp": "2025-11-17T14:30:10Z"
}
```

### 字段詳解

#### 識別字段 (Identification)

| 字段 | 類型 | 必需 | 範例 | 說明 |
|------|------|------|------|------|
| device_id | string | ✅ | "gw_001" | 設備唯一標識，不可變 |
| device_type | string | ✅ | "gateway" | 固定值："gateway" |
| device_name | string | ✅ | "客廳網關" | 人易讀名稱，可配置 |
| mac_address | string | ⭕ | "00:1A:2B:3C:4D:5E" | MAC 地址，用於識別 |

#### 網絡配置 (Network)

| 字段 | 類型 | 必需 | 範圍 | 說明 |
|------|------|------|------|------|
| ip_address | string | ⭕ | 192.168.x.x | WiFi 連接的 IP 地址 |
| rssi | number | ⭕ | -200 ~ 0 dBm | 信號強度（-45 最強，-90 很弱） |
| signal_quality | string | ⭕ | excellent/good/fair/poor | 計算得出的信號品質等級 |

#### 電源管理 (Power)

| 字段 | 類型 | 必需 | 範圍 | 說明 |
|------|------|------|------|------|
| battery_voltage | number | ⭕ | 2.0 ~ 5.0 V | 電池電壓，精度 0.1V |

#### 位置信息 (Position)

| 字段 | 類型 | 必需 | 範圍 | 說明 |
|------|------|------|------|------|
| position_x | number | ⭕ | 任意 | X 座標（米） |
| position_y | number | ⭕ | 任意 | Y 座標（米） |
| position_z | number | ⭕ | 0 ~ 5 | Z 座標 - 樓層高度（米） |

#### 設備狀態 (Status)

| 字段 | 類型 | 必需 | 值 | 說明 |
|------|------|------|------|------|
| status | string | ✅ | "online"/"offline" | 設備連接狀態 |
| is_bound | boolean | ✅ | true/false | 是否已綁定到 Floor |

#### 軟件版本 (Firmware)

| 字段 | 類型 | 必需 | 範例 | 說明 |
|------|------|------|------|------|
| fw_version | string | ⭕ | "v2.1.0" | 固件版本號 |
| config_mode | string | ⭕ | "auto"/"manual" | 配置模式 |

#### 時間戳 (Timestamps)

| 字段 | 類型 | 必需 | 格式 | 說明 |
|------|------|------|------|------|
| created_at | string | ⭕ | ISO 8601 | 設備創建時間 |
| last_seen | string | ⭕ | ISO 8601 | 最後一次看到該設備 |
| timestamp | string | ⭕ | ISO 8601 | 本次數據的時戳 |
| processing_timestamp | string | ⭕ | ISO 8601 | Dataflow 處理時間 |

**圖例說明：**
- ✅ = 必需，不能為 null
- ⭕ = 可選，可以為 null

---

## 🔌 Anchor 數據格式

### 完整字段列表

```json
{
  "device_id": "anchor_001",
  "device_type": "anchor",
  "device_name": "床位 1 標籤",
  "gateway_id": "gw_001",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  
  "position_x": 5.2,
  "position_y": 8.1,
  "position_z": 0.8,
  
  "status": "online",
  "battery_voltage": 3.2,
  "rssi": -52,
  "heart_rate": 72,
  "temperature": 36.5,
  "humidity": 45.2,
  
  "fw_update": false,
  "led_enabled": true,
  "ble_enabled": true,
  "is_initiator": false,
  
  "is_bound": true,
  "last_seen": "2025-11-17T14:35:00Z",
  "timestamp": "2025-11-17T14:35:00Z",
  "processing_timestamp": "2025-11-17T14:35:10Z"
}
```

### 字段詳解

#### 識別字段 (Identification)

| 字段 | 類型 | 必需 | 範例 | 說明 |
|------|------|------|------|------|
| device_id | string | ✅ | "anchor_001" | 標籤唯一標識 |
| device_type | string | ✅ | "anchor" | 固定值："anchor" |
| device_name | string | ✅ | "床位 1" | 人易讀名稱 |
| gateway_id | string | ✅ | "gw_001" | 所屬 Gateway ID |
| mac_address | string | ⭕ | "AA:BB:CC:DD:EE:FF" | MAC 地址 |

#### 生理數據 (Vitals)

| 字段 | 類型 | 必需 | 範圍 | 說明 |
|------|------|------|------|------|
| heart_rate | number | ⭕ | 30 ~ 200 bpm | 心率（每分鐘跳動次數） |
| temperature | number | ⭕ | 35 ~ 42 °C | 體溫（精度 0.1°C） |
| humidity | number | ⭕ | 0 ~ 100 % | 濕度（如有傳感器） |

#### 信號和電源 (Signal & Power)

| 字段 | 類型 | 必需 | 範圍 | 說明 |
|------|------|------|------|------|
| rssi | number | ⭕ | -200 ~ 0 dBm | 信號強度 |
| battery_voltage | number | ⭕ | 2.0 ~ 5.0 V | 電池電壓 |

#### 位置信息 (Position)

| 字段 | 類型 | 必需 | 說明 |
|------|------|------|------|
| position_x | number | ⭕ | X 座標（米）- UWB 定位 |
| position_y | number | ⭕ | Y 座標（米）- UWB 定位 |
| position_z | number | ⭕ | Z 座標（米）- 樓層 |

#### 設備配置 (Configuration)

| 字段 | 類型 | 必需 | 值 | 說明 |
|------|------|------|------|------|
| fw_update | boolean | ⭕ | true/false | 是否需要固件更新 |
| led_enabled | boolean | ⭕ | true/false | LED 燈是否啟用 |
| ble_enabled | boolean | ⭕ | true/false | 藍牙是否啟用 |
| is_initiator | boolean | ⭕ | true/false | 是否為 UWB 發起者 |

#### 狀態和時間 (Status & Time)

| 字段 | 類型 | 必需 | 說明 |
|------|------|------|------|
| status | string | ✅ | "online" 或 "offline" |
| is_bound | boolean | ✅ | 是否已綁定到人員 |
| last_seen | string | ⭕ | ISO 8601 格式 |
| timestamp | string | ⭕ | 數據時戳 |
| processing_timestamp | string | ⭕ | 處理時戳 |

---

## 📤 前端發送的格式

> 這是前端通過 MQTT 發送到 Pub/Sub 的原始格式（4層嵌套）
> Dataflow 會自動轉換為 FlattenedXxxData（2層）

### Gateway MQTT 消息

```json
{
  "gateway_id": "gw_001",
  "name": "客廳網關",
  "ip_address": "192.168.1.100",
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
  }
}
```

### Anchor MQTT 消息

```json
{
  "anchor_id": "anchor_001",
  "gateway_id": "gw_001",
  "cloudData": {
    "id": 1,
    "pub": {
      "msg": {
        "data": {
          "heart_rate": 72,
          "temperature": 36.5,
          "rssi": -52,
          "battery_voltage": 3.2
        }
      }
    },
    "fw_update": 0,
    "led": 1,
    "ble": 1,
    "initiator": 0,
    "position": {
      "x": 5.2,
      "y": 8.1,
      "z": 0.8
    }
  }
}
```

### 轉換規則

| 原始字段路徑 | 轉換後字段 | 說明 |
|-------------|----------|------|
| `cloudData.pub.msg.data.*` | 直接提升到第2層 | 深層嵌套的數據提升 |
| `cloudData.fw_update` (0/1) | `fw_update` (false/true) | 布爾值轉換 |
| `cloudData.led` (0/1) | `led_enabled` (false/true) | 布爾值轉換 |
| `cloudData.ble` (0/1) | `ble_enabled` (false/true) | 布爾值轉換 |
| `cloudData.initiator` (0/1) | `is_initiator` (false/true) | 布爾值轉換 |

---

## 💾 存儲層格式

### Redis (即時層)

**Key 命名規則：**

```
devices:gateway:{gateway_id}      # Gateway 最新數據
devices:anchor:{anchor_id}        # Anchor 最新數據
```

**Value 格式：**

```json
{
  "device_id": "gw_001",
  "device_type": "gateway",
  ...（完整的 FlattenedGatewayData）
}
```

**TTL：** 1 小時（自動過期）

**訪問速度：** < 1ms

### BigQuery (歷史層)

**表名稱：** `iot_events`

**主要列：**

| 列名 | 類型 | 用途 |
|------|------|------|
| timestamp | TIMESTAMP | 分區鍵（按天分區） |
| device_id | STRING | 叢集鍵 |
| device_type | STRING | 數據類型分類 |
| gateway_id | STRING | Gateway 關聯 |
| ... | ... | 所有 FlattenedXxxData 的字段 |

**分區：** 按天分區（自動清理 30 天外數據）

**叢集：** 按 device_id 和 device_type 叢集

**查詢速度：** 1-2 秒（1 小時數據）

### PostgreSQL (靜態層)

**表：** `tag_bindings`, `gateways`, `anchors`, 等

> 參考《Ktor 後端開發藍圖》的 PostgreSQL 部分

---

## 📝 使用示例

### 後端：讀取 FlattenedGatewayData

```python
# 從 Dataflow 獲取轉換後的數據
from src.models.gateway_data import FlattenedGatewayData

# 解析 JSON 成對象
raw_json = """
{
  "device_id": "gw_001",
  "device_type": "gateway",
  "battery_voltage": 3.7,
  "rssi": -45
}
"""

gateway_data = FlattenedGatewayData.from_json(raw_json)
print(gateway_data.battery_voltage)  # 輸出：3.7
```

### 前端：使用 TypeScript 類型

```typescript
// 導入類型（見 docs/typescript-types.ts）
import { FlattenedGatewayData, FlattenedAnchorData } from './types';

// IDE 自動完成
function displayGateway(gateway: FlattenedGatewayData) {
  return (
    <div>
      <h3>{gateway.device_name}</h3>
      <p>IP: {gateway.ip_address}</p>
      <p>信號: {gateway.rssi} dBm</p>
      <p>電池: {gateway.battery_voltage}V</p>
    </div>
  );
}
```

### 後端 API：查詢 Redis

```kotlin
// Ktor 後端查詢 Redis
val gateway = redis.get("devices:gateway:gw_001")
// 返回 FlattenedGatewayData JSON
```

### 後端 API：查詢 BigQuery

```kotlin
// 查詢 30 天內的設備數據
val query = """
  SELECT device_id, timestamp, battery_voltage, rssi
  FROM iot_events
  WHERE device_id = 'gw_001'
    AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  ORDER BY timestamp DESC
"""
```

---

## 📋 檢查清單

在開始開發前，確保你理解：

### 後端開發者

- [ ] 我理解 4層結構和 2層結構的區別
- [ ] 我知道 FlattenedGatewayData 和 FlattenedAnchorData 的所有字段
- [ ] 我知道如何從 Redis 查詢即時數據
- [ ] 我知道如何從 BigQuery 查詢歷史數據
- [ ] 我知道 MQTT 消息的原始格式

### 前端開發者

- [ ] 我已經複製了 docs/typescript-types.ts
- [ ] 我知道哪些字段是必需的，哪些是可選的
- [ ] 我知道 heart_rate 和 temperature 的取值範圍
- [ ] 我知道 rssi 和 battery_voltage 的含義
- [ ] 我知道如何在 React 中使用 FlattenedGatewayData 類型

---

## 🔗 相關文檔

- 📚 [ARCHITECTURE.md](./ARCHITECTURE.md) - 完整系統架構
- 💻 [typescript-types.ts](./typescript-types.ts) - TypeScript 類型定義（前端）
- 🔧 [BACKEND_INTEGRATION.md](./BACKEND_INTEGRATION.md) - 後端集成指南
- 🚀 [README.md](../README.md) - 快速開始指南

---

**最後更新：** 2025-11-17  
**狀態：** ✅ 完成



