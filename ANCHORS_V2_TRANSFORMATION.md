# Anchor JSON v2 2層轉換說明

## 轉換策略
- **原始 ≤2 層的字段**：保留原樣在頂層
- **原始 >2 層的字段**：拆解並移至 `cloud_data` 下，添加完整路徑前綴
- **重複字段名**：用前綴區分（如 `position` vs `cloud_data.position`）

---

## 輸入結構分析

### 原始數據層級
```
anchor (1層)
├── anchor_id ✅ (保留)
├── gateway_id ✅ (保留)
├── name ✅ (保留)
├── mac_address ✅ (保留)
├── position (2層) ✅ (保留)
├── status ✅ (保留)
├── lastSeen ✅ (保留)
├── isBound ✅ (保留)
└── cloudData (2層開始)
    ├── id ✅ (第2層，保留)
    ├── gateway_id ✅ (第2層，保留)
    ├── fw_update ✅ (第2層，保留)
    ├── led ✅ (第2層，保留)
    ├── ble ✅ (第2層，保留)
    ├── initiator ✅ (第2層，保留)
    ├── position (2層) ✅ (保留在cloud_data下)
    └── pub (3層開始) ❌ (需要拆解)
        └── msg (4層) ❌
            └── data (5層) ❌
                ├── battery_voltage → cloud_data.pub_msg_data_battery_voltage
                ├── rssi → cloud_data.pub_msg_data_rssi
                ├── heart_rate → cloud_data.pub_msg_data_heart_rate
                └── temperature → cloud_data.pub_msg_data_temperature
```

---

## 轉換過程示例

### Anchor #1: 完整對比

**輸入（原始）：**
```json
{
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
    "position": {
      "x": 5.2,
      "y": 8.1,
      "z": 0.8
    }
  },
  "position": {
    "x": 5.2,
    "y": 8.1,
    "z": 0.8
  },
  "status": "online",
  "lastSeen": "2025-11-17T14:30:00Z",
  "isBound": true
}
```

**輸出（v2 2層）：**
```json
{
  "anchor_id": "anchor_001",
  "gateway_id": "gw_001",
  "name": "Bed Anchor",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "status": "online",
  "lastSeen": "2025-11-17T14:30:00Z",
  "isBound": true,
  "position": {
    "x": 5.2,
    "y": 8.1,
    "z": 0.8
  },
  "cloud_data": {
    "id": 1,
    "gateway_id": 1,
    "fw_update": 0,
    "led": 1,
    "ble": 1,
    "initiator": 0,
    "position": {
      "x": 5.2,
      "y": 8.1,
      "z": 0.8
    },
    "pub_msg_data_battery_voltage": 3.2,
    "pub_msg_data_rssi": -52,
    "pub_msg_data_heart_rate": 72,
    "pub_msg_data_temperature": 36.5
  }
}
```

---

## 變化統計

| 字段名 | 層級 | 原始位置 | 轉換後位置 | 狀態 |
|--------|------|---------|-----------|------|
| `anchor_id` | 1 | 頂層 | 頂層 | ✅ 保留 |
| `gateway_id` | 1 | 頂層 | 頂層 | ✅ 保留 |
| `position` | 2 | 頂層 + `cloudData` | 頂層 + `cloud_data` | ✅ 保留 |
| `cloudData.id` | 2 | `cloudData.id` | `cloud_data.id` | ✅ 保留 |
| `cloudData.gateway_id` | 2 | `cloudData.gateway_id` | `cloud_data.gateway_id` | ✅ 保留 |
| `cloudData.pub.msg.data.*` | 5 | 深層嵌套 | `cloud_data.pub_msg_data_*` | ✅ 拆解+前綴 |

---

## 關鍵特性

### ✅ 數據保留
- 所有原始數據都被保留，**零數據丟失**
- 深層字段通過路徑前綴保持可追蹤性

### ✅ 結構簡化
- **原始層級**：最深 5 層 (`anchor > cloudData > pub > msg > data`)
- **轉換後**：最深 2 層 (`anchor > cloud_data` 或 `anchor > cloud_data > position`)
- **層級降低**：5 層 → 2 層 (-60% 複雜度)

### ✅ 重複字段處理
- 頂層 `position` 和 `cloud_data.position` 共存
- 通過命名空間（頂層 vs `cloud_data` 下）自動區分
- 無衝突，都能被正確識別

### ✅ 命名約定
- 拆解後的字段使用 `_` 連接路徑
- 示例：`pub.msg.data.battery_voltage` → `pub_msg_data_battery_voltage`
- 保持可讀性同時避免衝突

---

## 所有 3 個 Anchor 的輸出

見 `anchors_output_v2.json`

---

## 前端/後端使用指南

### 前端接收
```typescript
interface FlattenedAnchorData {
  anchor_id: string;
  gateway_id: string;
  name: string;
  mac_address: string;
  status: string;
  lastSeen: string;
  isBound: boolean;
  position: { x: number; y: number; z: number };
  cloud_data: {
    id: number;
    gateway_id: number;
    fw_update: number;
    led: number;
    ble: number;
    initiator: number;
    position: { x: number; y: number; z: number };
    pub_msg_data_battery_voltage: number;
    pub_msg_data_rssi: number;
    pub_msg_data_heart_rate: number;
    pub_msg_data_temperature: number;
  };
}
```

### 後端存儲
- **PostgreSQL**：存儲頂層字段 + `cloud_data` 作為 JSONB
- **Redis**：實時數據快取（TTL 5 分鐘），整個結構
- **BigQuery**：歷史數據（30 天），自動展平到列

---

## 驗證要點

✅ **層級檢查**：最深 2 層
✅ **數據完整**：所有原始字段保留
✅ **前綴正確**：深層字段包含完整路徑
✅ **無衝突**：重複字段名通過命名空間區分

