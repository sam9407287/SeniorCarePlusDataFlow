# Senior Care Plus DataFlow

🔄 使用 Apache Beam + Python 進行即時數據流轉換和處理

## 🎯 目的

將多層 IoT 數據（4層）轉換為扁平結構（2層），用於 BigQuery 分析和 Redis 實時操作。

---

## 📚 新開發者快速入門

> **第一次看這個 Repo？按順序讀這些文檔！**

### 🎯 5 分鐘了解核心概念

1. **讀這個 README**（2 分鐘）- 了解專案目的
2. **讀 [docs/DATA_FORMAT_GUIDE.md](docs/DATA_FORMAT_GUIDE.md)**（3 分鐘）
   - 看「快速參考表」了解所有字段
   - Gateway vs Anchor 的區別

### 💻 15 分鐘根據你的角色選擇

**如果你是前端開發者：**
- ✅ 複製 [docs/typescript-types.ts](docs/typescript-types.ts)
- ✅ 在 React 項目中導入使用
- ✅ 享受 IDE 自動完成和類型檢查
- 📖 文檔：[DATA_FORMAT_GUIDE.md](docs/DATA_FORMAT_GUIDE.md)

**如果你是後端開發者：**
- ✅ 讀 [docs/BACKEND_INTEGRATION.md](docs/BACKEND_INTEGRATION.md)
- ✅ 查看 Kotlin/Python 集成示例
- ✅ 了解如何查詢 Redis 和 BigQuery
- 📖 參考：[src/models/](src/models/)

**如果你是架構師：**
- ✅ 讀 [ARCHITECTURE.md](ARCHITECTURE.md) - 完整系統設計
- ✅ 看 [docs/DATA_FORMAT_GUIDE.md](docs/DATA_FORMAT_GUIDE.md) - 數據流向
- ✅ 查看 [DELIVERY_CHECKLIST.md](DELIVERY_CHECKLIST.md) - 完整功能

### 🧪 測試示例數據

```bash
# 查看測試數據
cat test_data/gateways.json
cat test_data/anchors.json

# 本地運行轉換
python -m src.main --runner DirectRunner \
  --pipeline gateway \
  --input-type file \
  --input-file test_data/gateways.json
```

### 📋 完整文檔地圖

| 文檔 | 適合人群 | 用時 |
|------|---------|------|
| 📚 [DATA_FORMAT_GUIDE.md](docs/DATA_FORMAT_GUIDE.md) | 所有開發者 | 5 分鐘 |
| 💻 [typescript-types.ts](docs/typescript-types.ts) | 前端開發者 | 複製即用 |
| 🔧 [BACKEND_INTEGRATION.md](docs/BACKEND_INTEGRATION.md) | 後端開發者 | 20 分鐘 |
| 📐 [ARCHITECTURE.md](ARCHITECTURE.md) | 架構師/技術負責 | 30 分鐘 |
| 📖 [README.md](README.md) | 所有人 | 10 分鐘 |

---

```
4層結構 → 2層結構
┌─────────────────────────────────────┐
│  cloudData (第1層)                  │
│  ├── pub (第2層)                    │
│  │   └── msg (第3層)                │
│  │       └── data (第4層)           │
│  └── ...其他字段                    │
└─────────────────────────────────────┘
        ↓ Dataflow 轉換
┌─────────────────────────────────────┐
│  第1層：設備基本信息                 │
│  ├── device_id                      │
│  ├── gateway_id                     │
│  └── ...                            │
│                                     │
│  第2層：事件數據                     │
│  ├── battery_voltage                │
│  ├── rssi                           │
│  └── ...                            │
└─────────────────────────────────────┘
```

## 📂 目錄結構

```
SeniorCarePlusDataFlow/
├── src/
│   ├── __init__.py
│   ├── main.py                          # 主入口
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── gateway_flattening.py        # Gateway 數據轉換管道
│   │   ├── anchor_flattening.py         # Anchor 數據轉換管道
│   │   └── unified_pipeline.py          # 統一管道
│   ├── transforms/
│   │   ├── __init__.py
│   │   ├── flatten_transform.py         # 扁平化轉換
│   │   ├── validation_transform.py      # 數據驗證
│   │   ├── enrichment_transform.py      # 數據增強
│   │   └── custom_coders.py             # 自訂編碼器
│   ├── models/
│   │   ├── __init__.py
│   │   ├── gateway_data.py              # Gateway 數據模型
│   │   ├── anchor_data.py               # Anchor 數據模型
│   │   └── flattened_data.py            # 扁平化數據模型
│   ├── io/
│   │   ├── __init__.py
│   │   ├── pubsub_source.py             # Pub/Sub 源
│   │   ├── bigquery_sink.py             # BigQuery 輸出
│   │   └── redis_sink.py                # Redis 輸出
│   ├── config/
│   │   ├── __init__.py
│   │   └── pipeline_config.py           # 管道配置
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                    # 日誌工具
│       └── helpers.py                   # 幫助函數
├── tests/
│   ├── __init__.py
│   ├── test_transforms.py               # 轉換測試
│   └── test_pipelines.py                # 管道測試
├── config/
│   ├── dev.yaml                         # 開發環境配置
│   ├── prod.yaml                        # 生產環境配置
│   └── test.yaml                        # 測試環境配置
├── scripts/
│   ├── run_local.sh                     # 本地執行
│   ├── run_dataflow.sh                  # 在 GCP Dataflow 上執行
│   └── setup_gcp.sh                     # GCP 環境初始化
├── docs/
│   ├── ARCHITECTURE.md                  # 架構說明
│   ├── DEPLOYMENT.md                    # 部署指南
│   └── EXAMPLES.md                      # 使用示例
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

## 🚀 快速開始

### 1️⃣ 安裝依賴

```bash
# 建立虛擬環境
python3.9 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安裝依賴
pip install -r requirements.txt
```

### 2️⃣ 本地開發執行

```bash
python src/main.py \
  --runner DirectRunner \
  --input-type file \
  --input-file test_data/gateway_data.json
```

### 3️⃣ 提交到 GCP Dataflow

```bash
python src/main.py \
  --runner DataflowRunner \
  --project your-gcp-project \
  --temp-location gs://your-bucket/temp \
  --input-type pubsub \
  --input-topic projects/your-project/topics/gateway-events
```

## 🔧 配置

編輯 `config/prod.yaml` 進行生產部署配置：

```yaml
project_id: your-gcp-project-id
region: asia-east1
gcs_temp_bucket: gs://your-bucket/temp
gcs_staging_bucket: gs://your-bucket/staging

sources:
  gateway_pubsub: projects/your-project/topics/gateway-events
  anchor_pubsub: projects/your-project/topics/anchor-events

sinks:
  bigquery_gateway: your-project:analytics.gateway_events
  bigquery_anchor: your-project:analytics.anchor_events
  redis_host: redis.example.com
  redis_port: 6379
```

## 📊 數據流

```
Pub/Sub (原始 4層數據)
    ↓
[驗證轉換]
    ↓
[扁平化轉換]
    ↓
[數據增強]
    ↓
┌───────────────────────────┐
│   輸出                    │
├───────────────────────────┤
│ BigQuery (冷數據)         │
│ Redis (熱數據)            │
│ GCS (備份)                │
└───────────────────────────┘
```

## 🧪 測試

```bash
# 執行所有測試
pytest tests/ -v

# 執行特定測試
pytest tests/test_transforms.py::test_flatten_gateway -v

# 生成覆蓋報告
pytest tests/ --cov=src
```

## 📈 監控

部署到 Dataflow 後，在 GCP Console 查看：
- 管道狀態：https://console.cloud.google.com/dataflow
- 日誌：Cloud Logging
- 指標：Cloud Monitoring

## 🔐 GCP 設置

1. 建立 GCP 項目
2. 啟用以下 API：
   - Cloud Pub/Sub
   - Cloud Dataflow
   - BigQuery
   - Cloud Storage
   - Cloud Logging

3. 建立服務帳戶並下載金鑰
4. 設置環境變數：

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

## 📚 相關文檔

- [架構設計](docs/ARCHITECTURE.md)
- [部署指南](docs/DEPLOYMENT.md)
- [使用示例](docs/EXAMPLES.md)

## 🛠️ 開發工具

```bash
# 代碼格式化
black src/ tests/

# 型別檢查
mypy src/

# Linting
flake8 src/ tests/

# 所有檢查
make lint
```

## 📝 許可證

MIT

## 👥 貢獻者

Senior Care Plus Team


