# 🔧 後端集成指南

> 本指南適合後端開發者（Kotlin/Java/Python/Go）集成 Dataflow 轉換後的數據

## 📖 目錄

- [概述](#概述)
- [Kotlin (Ktor) 集成](#kotlin-ktor-集成)
- [Python 集成](#python-集成)
- [數據驗證](#數據驗證)
- [常見問題](#常見問題)

---

## 概述

### 你的後端應該做什麼？

```
┌─────────────────────────────────────────────┐
│ MQTT 消息 (原始 4層數據)                    │
│  └─ Cloud Pub/Sub                           │
│     └─ Cloud Dataflow (Beam Pipeline)       │
│        ├─ 驗證                              │
│        ├─ 去重                              │
│        ├─ 扁平化 (4層 → 2層)              │
│        └─ 分流寫入                          │
│           ├─ Redis (熱層)                  │
│           └─ BigQuery (冷層)               │
│                                             │
│ 【你的後端只需要讀取】                    │
│ ├─ Redis: 最新數據                          │
│ ├─ BigQuery: 歷史數據                       │
│ └─ PostgreSQL: 靜態配置                     │
└─────────────────────────────────────────────┘
```

### 數據流向

```
前端/客戶端
    ↓
後端 API (Ktor/Spring/FastAPI)
    ├─→ 查詢 PostgreSQL (用戶權限驗證)
    ├─→ 查詢 Redis (即時數據)
    ├─→ 查詢 BigQuery (歷史數據)
    └─→ 返回 JSON 給前端

WebSocket 推送
    ├─→ 後端監聽 Redis Channel
    └─→ 實時推送給前端
```

---

## Kotlin (Ktor) 集成

### 1. 依賴配置

```kotlin
// build.gradle.kts
dependencies {
    // Redis
    implementation("io.lettuce:lettuce-core:6.3.1.RELEASE")
    implementation("org.redisson:redisson:3.24.3")
    
    // Google Cloud
    implementation("com.google.cloud:google-cloud-bigquery:2.37.0")
    implementation("com.google.cloud:google-cloud-storage:2.37.0")
    
    // JSON 序列化
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
}
```

### 2. 數據模型（對應 Python FlattenedXxxData）

```kotlin
package com.example.data.models

import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName

/**
 * 扁平化後的 Gateway 數據（2層結構）
 * 
 * 對應 Python 的 FlattenedGatewayData
 */
@Serializable
data class FlattenedGatewayData(
    // 第1層：設備基本信息
    val device_id: String,
    val device_type: String = "gateway",
    val device_name: String,
    
    // 網絡配置
    val ip_address: String? = null,
    val mac_address: String? = null,
    
    // 位置信息
    val position_x: Double? = null,
    val position_y: Double? = null,
    val position_z: Double? = null,
    
    // 設備狀態
    val status: String = "unknown",
    val is_bound: Boolean = false,
    val created_at: String? = null,
    val last_seen: String? = null,
    
    // 第2層：事件數據
    val battery_voltage: Double? = null,
    val rssi: Int? = null,
    val signal_quality: String? = null,
    val fw_version: String? = null,
    val config_mode: String? = null,
    
    // 時間戳
    val timestamp: String? = null,
    val processing_timestamp: String? = null
)

/**
 * 扁平化後的 Anchor 數據（2層結構）
 * 
 * 對應 Python 的 FlattenedAnchorData
 */
@Serializable
data class FlattenedAnchorData(
    // 第1層：設備基本信息
    val device_id: String,
    val device_type: String = "anchor",
    val device_name: String,
    val gateway_id: String? = null,
    val mac_address: String? = null,
    
    // 位置信息
    val position_x: Double? = null,
    val position_y: Double? = null,
    val position_z: Double? = null,
    
    // 設備狀態
    val status: String = "unknown",
    val is_bound: Boolean = false,
    val last_seen: String? = null,
    
    // 第2層：傳感器數據
    val battery_voltage: Double? = null,
    val rssi: Int? = null,
    val heart_rate: Int? = null,
    val temperature: Double? = null,
    val humidity: Double? = null,
    
    // 設備配置
    val fw_update: Boolean? = null,
    val led_enabled: Boolean? = null,
    val ble_enabled: Boolean? = null,
    val is_initiator: Boolean? = null,
    
    // 時間戳
    val timestamp: String? = null,
    val processing_timestamp: String? = null
)
```

### 3. Redis 服務（讀取即時數據）

```kotlin
package com.example.data.services

import io.lettuce.core.RedisClient
import kotlinx.serialization.json.Json
import com.example.data.models.FlattenedGatewayData
import com.example.data.models.FlattenedAnchorData

class RedisDeviceService(private val redisClient: RedisClient) {
    
    private val json = Json { ignoreUnknownKeys = true }
    
    /**
     * 獲取最新的 Gateway 數據
     */
    suspend fun getLatestGateway(gatewayId: String): FlattenedGatewayData? {
        val connection = redisClient.connect().coroutines()
        val rawData = connection.get("devices:gateway:$gatewayId") ?: return null
        return json.decodeFromString<FlattenedGatewayData>(rawData)
    }
    
    /**
     * 批量獲取多個 Gateway 最新數據
     */
    suspend fun getLatestGatewayBatch(gatewayIds: List<String>): Map<String, FlattenedGatewayData> {
        val connection = redisClient.connect().coroutines()
        val keys = gatewayIds.map { "devices:gateway:$it" }
        val results = connection.mget(*keys.toTypedArray())
        
        return results.mapNotNull { (key, value) ->
            if (value != null) {
                val id = key.removePrefix("devices:gateway:")
                id to json.decodeFromString<FlattenedGatewayData>(value)
            } else {
                null
            }
        }.toMap()
    }
    
    /**
     * 獲取最新的 Anchor 數據
     */
    suspend fun getLatestAnchor(anchorId: String): FlattenedAnchorData? {
        val connection = redisClient.connect().coroutines()
        val rawData = connection.get("devices:anchor:$anchorId") ?: return null
        return json.decodeFromString<FlattenedAnchorData>(rawData)
    }
    
    /**
     * 批量獲取多個 Anchor 最新數據
     */
    suspend fun getLatestAnchorBatch(anchorIds: List<String>): Map<String, FlattenedAnchorData> {
        val connection = redisClient.connect().coroutines()
        val keys = anchorIds.map { "devices:anchor:$it" }
        val results = connection.mget(*keys.toTypedArray())
        
        return results.mapNotNull { (key, value) ->
            if (value != null) {
                val id = key.removePrefix("devices:anchor:")
                id to json.decodeFromString<FlattenedAnchorData>(value)
            } else {
                null
            }
        }.toMap()
    }
}
```

### 4. BigQuery 服務（查詢歷史數據）

```kotlin
package com.example.data.services

import com.google.cloud.bigquery.BigQuery
import com.google.cloud.bigquery.QueryJobConfiguration
import com.example.data.models.FlattenedGatewayData
import com.example.data.models.FlattenedAnchorData
import kotlinx.serialization.json.Json

class BigQueryDeviceService(private val bigquery: BigQuery) {
    
    private val json = Json { ignoreUnknownKeys = true }
    
    /**
     * 查詢 Gateway 歷史數據
     */
    suspend fun getGatewayHistory(
        gatewayId: String,
        startTime: Long,  // 毫秒
        endTime: Long     // 毫秒
    ): List<FlattenedGatewayData> {
        val query = """
            SELECT 
                device_id, device_type, device_name,
                ip_address, mac_address,
                position_x, position_y, position_z,
                status, is_bound,
                battery_voltage, rssi, signal_quality,
                fw_version, config_mode,
                timestamp
            FROM `iot_events`
            WHERE 
                device_id = '$gatewayId'
                AND device_type = 'gateway'
                AND UNIX_MILLIS(timestamp) BETWEEN $startTime AND $endTime
            ORDER BY timestamp DESC
        """.trimIndent()
        
        val queryJob = bigquery.query(QueryJobConfiguration.newBuilder(query).build())
        val results = mutableListOf<FlattenedGatewayData>()
        
        for (row in queryJob.getQueryResults().iterateAll()) {
            // 轉換為 Kotlin 對象
            results.add(
                FlattenedGatewayData(
                    device_id = row.get("device_id").stringValue,
                    device_name = row.get("device_name").stringValue,
                    // ... 其他字段
                )
            )
        }
        
        return results
    }
    
    /**
     * 查詢 Anchor 歷史生理數據（聚合）
     */
    suspend fun getAnchorVitalsAggregated(
        anchorId: String,
        startTime: Long,
        endTime: Long,
        intervalMinutes: Int = 5  // 5 分鐘聚合一次
    ): List<Map<String, Any>> {
        val query = """
            SELECT 
                TIMESTAMP_TRUNC(timestamp, MINUTE) as time_bucket,
                AVG(heart_rate) as avg_heart_rate,
                MIN(heart_rate) as min_heart_rate,
                MAX(heart_rate) as max_heart_rate,
                AVG(temperature) as avg_temperature,
                COUNT(*) as sample_count
            FROM `iot_events`
            WHERE 
                device_id = '$anchorId'
                AND device_type = 'anchor'
                AND UNIX_MILLIS(timestamp) BETWEEN $startTime AND $endTime
            GROUP BY time_bucket
            ORDER BY time_bucket DESC
        """.trimIndent()
        
        val queryJob = bigquery.query(QueryJobConfiguration.newBuilder(query).build())
        val results = mutableListOf<Map<String, Any>>()
        
        for (row in queryJob.getQueryResults().iterateAll()) {
            results.add(
                mapOf(
                    "time" to row.get("time_bucket").timestampValue,
                    "avg_heart_rate" to (row.get("avg_heart_rate").doubleValue?.toInt()),
                    "min_heart_rate" to (row.get("min_heart_rate").doubleValue?.toInt()),
                    "max_heart_rate" to (row.get("max_heart_rate").doubleValue?.toInt()),
                    "avg_temperature" to row.get("avg_temperature").doubleValue,
                    "sample_count" to row.get("sample_count").longValue
                )
            )
        }
        
        return results
    }
}
```

### 5. Ktor 路由（API 端點）

```kotlin
package com.example.routes

import io.ktor.server.routing.*
import io.ktor.server.response.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import com.example.data.services.RedisDeviceService
import com.example.data.services.BigQueryDeviceService

fun Route.deviceRoutes(
    redisService: RedisDeviceService,
    bigQueryService: BigQueryDeviceService
) {
    
    // ========== REST API 端點 ==========
    
    get("/devices/gateway/{gatewayId}") {
        val gatewayId = call.parameters["gatewayId"] ?: return@get call.respond(mapOf("error" to "Missing gatewayId"))
        
        // 查詢 Redis 獲取最新數據
        val gateway = redisService.getLatestGateway(gatewayId)
        
        if (gateway != null) {
            call.respond(gateway)
        } else {
            call.respond(mapOf("error" to "Gateway not found"))
        }
    }
    
    get("/devices/gateway/{gatewayId}/history") {
        val gatewayId = call.parameters["gatewayId"] ?: return@get call.respond(mapOf("error" to "Missing gatewayId"))
        val startTime = call.request.queryParameters["start"]?.toLong() ?: return@get call.respond(mapOf("error" to "Missing start"))
        val endTime = call.request.queryParameters["end"]?.toLong() ?: return@get call.respond(mapOf("error" to "Missing end"))
        
        // 查詢 BigQuery 獲取歷史數據
        val history = bigQueryService.getGatewayHistory(gatewayId, startTime, endTime)
        call.respond(mapOf("data" to history, "count" to history.size))
    }
    
    get("/devices/anchor/{anchorId}/vitals") {
        val anchorId = call.parameters["anchorId"] ?: return@get call.respond(mapOf("error" to "Missing anchorId"))
        val startTime = call.request.queryParameters["start"]?.toLong() ?: return@get call.respond(mapOf("error" to "Missing start"))
        val endTime = call.request.queryParameters["end"]?.toLong() ?: return@get call.respond(mapOf("error" to "Missing end"))
        
        // 查詢 BigQuery 聚合數據
        val vitals = bigQueryService.getAnchorVitalsAggregated(anchorId, startTime, endTime)
        call.respond(mapOf("data" to vitals, "count" to vitals.size))
    }
    
    // ========== WebSocket 即時推送 ==========
    
    webSocket("/ws/devices/gateway/{gatewayId}") {
        val gatewayId = call.parameters["gatewayId"] ?: return@webSocket close(CloseReason(CloseReason.Codes.CANNOT_ACCEPT))
        
        // 初始發送最新數據
        val latestGateway = redisService.getLatestGateway(gatewayId)
        if (latestGateway != null) {
            send(Frame.Text(json.encodeToString(latestGateway)))
        }
        
        // 訂閱 Redis Channel（每 5 秒推送新數據）
        // 實現方式取決於你的 Redis 客戶端
        // 例子（使用 Redisson）：
        // val topic = redisson.getTopic("devices:gateway:$gatewayId:updates")
        // topic.addListener(String::class.java) { msg ->
        //     send(Frame.Text(msg))
        // }
    }
}
```

---

## Python 集成

### 1. 讀取 FlattenedGatewayData

```python
from src.models.gateway_data import FlattenedGatewayData
import json

# 從 Redis 或 BigQuery 獲取的 JSON 字符串
gateway_json = """
{
  "device_id": "gw_001",
  "device_type": "gateway",
  "device_name": "客廳網關",
  "battery_voltage": 3.7,
  "rssi": -45
}
"""

# 轉換為 Python 對象
gateway = FlattenedGatewayData.from_json(gateway_json)

# 訪問字段
print(f"設備名: {gateway.device_name}")
print(f"電池: {gateway.battery_voltage}V")
print(f"信號: {gateway.rssi} dBm")

# 轉回 JSON（用於 API 返回）
api_response = gateway.to_json()
```

### 2. 驗證數據

```python
from src.transforms.validation_transform import ValidateGatewayTransform

# 使用 Dataflow 的驗證邏輯
validator = ValidateGatewayTransform()

gateway_dict = {
    "device_id": "gw_001",
    "device_type": "gateway",
    "battery_voltage": 3.7,
    "rssi": -45
}

# 驗證
for result in validator.process(gateway_dict):
    if result.get("is_valid"):
        print("✓ 數據有效")
    else:
        print(f"✗ 驗證失敗: {result.get('validation_errors')}")
```

---

## 數據驗證

### Gateway 驗證規則

| 字段 | 類型 | 必需 | 驗證規則 |
|------|------|------|---------|
| device_id | string | ✅ | 非空 |
| device_type | string | ✅ | 必須是 "gateway" |
| battery_voltage | number | ⭕ | 2.0 ~ 5.0 V |
| rssi | number | ⭕ | -200 ~ 0 dBm |

### Anchor 驗證規則

| 字段 | 類型 | 必需 | 驗證規則 |
|------|------|------|---------|
| device_id | string | ✅ | 非空 |
| device_type | string | ✅ | 必須是 "anchor" |
| heart_rate | number | ⭕ | 30 ~ 200 bpm |
| temperature | number | ⭕ | 35 ~ 42 °C |
| rssi | number | ⭕ | -200 ~ 0 dBm |

---

## 常見問題

### Q1: 我需要自己實現 Pipeline 嗎？

**A:** 不需要！Dataflow Pipeline 已經完成了。你的後端只需要：
- ✅ 讀取 Redis 中的即時數據
- ✅ 查詢 BigQuery 中的歷史數據
- ❌ 不需要寫入 Redis 或 BigQuery（Dataflow 做）
- ❌ 不需要驗證或去重（Dataflow 做）

### Q2: 如何在本地開發時測試？

**A:** 使用 test_data 中的示例：

```kotlin
// test_data/gateways.json
val testGateway = FlattenedGatewayData.from_json("""
{
  "device_id": "gw_001",
  "device_type": "gateway",
  "device_name": "測試網關",
  "battery_voltage": 3.7,
  "rssi": -45
}
""")

// 測試 API 端點
client.get("/devices/gateway/gw_001") {
    // 模擬返回 testGateway
}
```

### Q3: Redis 和 BigQuery 查詢的差異？

**A:**

| 場景 | 使用 Redis | 使用 BigQuery |
|------|----------|--------------|
| 查詢最新 1 分鐘數據 | ✅ 快 (< 1ms) | ❌ 可能過度查詢 |
| 查詢過去 1 小時數據 | ✅ 快 (< 100ms) | ⭕ 可以但慢些 |
| 查詢 1 天前的數據 | ❌ 已過期 | ✅ 快 (< 2s) |
| 統計分析（聚合） | ❌ 不支持 | ✅ 最佳選擇 |

### Q4: 如何處理 Redis 宕機？

**A:** 自動 fallback：

```kotlin
suspend fun getGatewayData(gatewayId: String): FlattenedGatewayData? {
    return try {
        // 先嘗試 Redis
        redisService.getLatestGateway(gatewayId)
    } catch (e: Exception) {
        logger.warn("Redis 不可用，使用 BigQuery")
        // 如果失敗，查詢 BigQuery 最新 1 小時內的數據
        bigQueryService.getGatewayHistory(
            gatewayId,
            System.currentTimeMillis() - 3600000,
            System.currentTimeMillis()
        ).firstOrNull()
    }
}
```

### Q5: 數據更新延遲多久？

**A:**

| 來源 | 延遲 | 說明 |
|------|------|------|
| Redis | < 5 秒 | Dataflow 實時寫入 |
| BigQuery | < 1 分鐘 | Dataflow 批次寫入 |
| WebSocket | < 200ms | 即時推送 |

---

## 🔗 相關資源

- 📊 [DATA_FORMAT_GUIDE.md](./DATA_FORMAT_GUIDE.md) - 數據格式完整說明
- 📐 [ARCHITECTURE.md](./ARCHITECTURE.md) - 系統架構
- 🐍 [Python 模型](../src/models/) - Python 數據模型
- 🧪 [測試數據](../test_data/) - 示例 JSON 數據

---

**最後更新：** 2025-11-17  
**狀態：** ✅ 完成

