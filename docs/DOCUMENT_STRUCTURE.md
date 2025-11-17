# 📁 文檔結構指南

> 本文檔專為防止 AI 和新開發者混亂而編寫

## 🎯 快速導航

### 我應該讀哪份文檔？

```
├─ 想快速了解項目？
│  └─ 讀 README.md (5 分鐘)
│
├─ 想理解數據格式？
│  └─ 讀 docs/DATA_FORMAT_GUIDE.md (10 分鐘)
│
├─ 我是前端開發者
│  ├─ 複製 docs/typescript-types.ts
│  └─ 讀 docs/DATA_FORMAT_GUIDE.md 中的「使用示例」
│
├─ 我是後端開發者
│  └─ 讀 docs/BACKEND_INTEGRATION.md (20 分鐘)
│
├─ 我是架構師
│  ├─ 讀 ARCHITECTURE.md (30 分鐘)
│  ├─ 讀 docs/DATA_FORMAT_GUIDE.md 理解數據流
│  └─ 讀 DELIVERY_CHECKLIST.md 查看完成情況
│
└─ 我要修改代碼
   ├─ 修改 Python 模型 → src/models/
   ├─ 修改轉換邏輯 → src/transforms/
   └─ 修改 Pipeline → src/pipelines/
```

---

## 📚 每份文檔的目的

### README.md
- **用途**：項目總覽和快速開始
- **適合人群**：所有人
- **包含內容**：
  - 項目簡介
  - 5 分鐘新開發者入門指南
  - 快速開始步驟
  - 文檔地圖

### docs/DATA_FORMAT_GUIDE.md
- **用途**：所有數據格式的完整說明
- **適合人群**：前端、後端、架構師
- **包含內容**：
  - Gateway vs Anchor 對比表
  - 完整字段列表和詳解
  - 4層 vs 2層結構對比
  - 存儲層（Redis/BigQuery）格式
  - 使用示例
  - 檢查清單

### docs/typescript-types.ts
- **用途**：前端可直接複製使用的 TypeScript 類型
- **適合人群**：前端開發者
- **特性**：
  - ✅ 可直接複製/貼上到 React 項目
  - ✅ 包含完整類型定義
  - ✅ 包含常數、守衛函數、工具類型
  - ✅ 有 JSDoc 註釋

### docs/BACKEND_INTEGRATION.md
- **用途**：後端如何集成 Dataflow 轉換後的數據
- **適合人群**：Kotlin/Java/Python 後端開發者
- **包含內容**：
  - Kotlin (Ktor) 集成示例
  - Python 集成示例
  - Redis 和 BigQuery 查詢方法
  - 常見問題解答

### ARCHITECTURE.md
- **用途**：完整系統架構和設計細節
- **適合人群**：架構師、技術負責人
- **包含內容**：
  - 系統架構圖
  - 數據流向詳解
  - 模塊設計和依賴關係
  - Pipeline 流程
  - 集成方案
  - 性能考量

### GITHUB_SETUP.md
- **用途**：GitHub 倉庫設置指南
- **適合人群**：所有團隊成員
- **包含內容**：
  - SSH 密鑰設置
  - Clone 和初始化步驟
  - 提交和推送指南

### DELIVERY_CHECKLIST.md
- **用途**：項目交付前的完整檢查清單
- **適合人群**：項目經理、技術負責人
- **包含內容**：
  - 功能完成清單
  - 代碼質量檢查
  - 文檔完整性檢查
  - 部署準備清單

### docs/DOCUMENT_STRUCTURE.md（本文件）
- **用途**：防止 AI 和新開發者對文檔結構混亂
- **適合人群**：所有人（特別是 AI）
- **包含內容**：
  - 快速導航地圖
  - 每份文檔的目的和內容
  - 禁止事項

---

## ⚠️ 防止 AI 混亂的規則

### ✅ 允許做的事

1. **跨檔案引用**
   - ✅ 在 README.md 中引用 DATA_FORMAT_GUIDE.md
   - ✅ 在 BACKEND_INTEGRATION.md 中引用 DATA_FORMAT_GUIDE.md
   - ✅ 使用 Markdown 鏈接：`[文件名](./路徑)`

2. **重複內容**
   - ✅ 在 DATA_FORMAT_GUIDE.md 和 BACKEND_INTEGRATION.md 中都有 JSON 示例
   - ✅ 在 README.md 和 DATA_FORMAT_GUIDE.md 中都有快速參考表
   - 原因：不同角色從不同入口點進來

3. **角色特定文檔**
   - ✅ typescript-types.ts 是專為前端的
   - ✅ BACKEND_INTEGRATION.md 是專為後端的
   - 原因：前後端有完全不同的需求

### ❌ 禁止做的事

1. **創建新的主文檔**
   - ❌ 不要創建 FRONTEND_GUIDE.md（改用 README.md 的角色導航）
   - ❌ 不要創建 ARCHITECTURE_DETAILED.md（用 ARCHITECTURE.md）
   - ❌ 不要創建 DATA_SCHEMA.md（用 DATA_FORMAT_GUIDE.md）

2. **分散相同內容**
   - ❌ 不要在 3 個地方都寫一份 Gateway 數據格式說明
   - ✅ 改成：在 DATA_FORMAT_GUIDE.md 寫一次，其他文檔鏈接過去

3. **模糊的命名**
   - ❌ 不要創建 GUIDE.md、NOTES.md、INFO.md
   - ✅ 改成：具體的名稱如 BACKEND_INTEGRATION.md、DATA_FORMAT_GUIDE.md

4. **無序的信息組織**
   - ❌ 不要把 TypeScript 類型混在 Markdown 中
   - ✅ 改成：typescript-types.ts 是獨立的 .ts 文件

---

## 📂 檔案結構圖

```
SeniorCarePlusDataFlow/
│
├── README.md
│   └─ 【入口點】新人從這開始
│   └─ 包含快速導航
│   └─ 指引到其他文檔
│
├── ARCHITECTURE.md
│   └─ 【系統設計】完整架構
│
├── docs/
│   ├── DATA_FORMAT_GUIDE.md ⭐️ 【核心文檔】
│   │   ├─ 快速參考表
│   │   ├─ Gateway 格式詳解
│   │   ├─ Anchor 格式詳解
│   │   ├─ 前端發送格式
│   │   └─ 存儲層格式
│   │
│   ├── typescript-types.ts ⭐️ 【前端專用】
│   │   ├─ 可直接複製/貼上
│   │   ├─ 完整的類型定義
│   │   ├─ 類型守衛函數
│   │   └─ React Props 類型
│   │
│   ├── BACKEND_INTEGRATION.md ⭐️ 【後端專用】
│   │   ├─ Kotlin 集成
│   │   ├─ Python 集成
│   │   ├─ Redis 查詢
│   │   └─ BigQuery 查詢
│   │
│   ├── GITHUB_SETUP.md
│   │   └─ GitHub 倉庫設置
│   │
│   └── DOCUMENT_STRUCTURE.md 👈 【本文件】
│       └─ 防止 AI 混亂的指南
│
├── GITHUB_SETUP.md （已刪除，改在 docs/ 下）
├── DELIVERY_CHECKLIST.md
│   └─ 項目交付清單
│
├── src/
│   ├── models/
│   │   ├── gateway_data.py
│   │   │   └─ 包含 FlattenedGatewayData 定義
│   │   └── anchor_data.py
│   │       └─ 包含 FlattenedAnchorData 定義
│   │
│   ├── transforms/
│   │   ├── flatten_transform.py
│   │   │   └─ 4層 → 2層轉換邏輯
│   │   └── validation_transform.py
│   │       └─ 數據驗證邏輯
│   │
│   └── pipelines/
│       ├── gateway_flattening.py
│       └── anchor_flattening.py
│
└── test_data/
    ├── gateways.json
    │   └─ 3 個 Gateway 示例（4層原始格式）
    └── anchors.json
        └─ 3 個 Anchor 示例（4層原始格式）
```

---

## 🔄 文檔間的關係

```
新開發者打開 Repo
    ↓
讀 README.md
    ↓
    ├─→ 是前端嗎？ → 讀 DATA_FORMAT_GUIDE.md → 複製 typescript-types.ts
    ├─→ 是後端嗎？ → 讀 DATA_FORMAT_GUIDE.md → 讀 BACKEND_INTEGRATION.md
    └─→ 是架構師嗎？ → 讀 ARCHITECTURE.md → 讀 DELIVERY_CHECKLIST.md
```

---

## 🎯 AI 助手的使用指南

### 當 AI 問「我應該在哪寫這份文檔？」

1. **如果是通用知識**（所有人都需要）
   - 📝 寫到 docs/DATA_FORMAT_GUIDE.md
   - 示例：字段詳解、驗證規則

2. **如果是角色特定知識**（只有某類人需要）
   - 📝 寫到 docs/{ROLE}_INTEGRATION.md 或單獨文件
   - 示例：前端 → typescript-types.ts、後端 → BACKEND_INTEGRATION.md

3. **如果是快速參考**（需要在 IDE 中看）
   - 📝 寫成 .ts 或 .py 文件帶代碼
   - 示例：typescript-types.ts

### 當 AI 想創建新文檔時

**先問 3 個問題：**

1. ❓ 是否已經有類似的文檔？
   - 是 → 添加到現有文檔，不要創建新文檔
   - 否 → 继续

2. ❓ 這份內容適合所有人嗎？
   - 是 → 放在 docs/ 下，README 中添加鏈接
   - 否 → 創建角色特定文檔

3. ❓ 內容需要 IDE 自動完成嗎？
   - 是 → 創建 .ts/.py 文件
   - 否 → 創建 .md 文檔

---

## ✅ 文檔完整性檢查清單

在編輯任何文檔前，檢查：

- [ ] 我知道這份文檔的受眾是誰
- [ ] 我知道這份文檔的目的
- [ ] 我知道是否會與其他文檔重複
- [ ] 我知道如何從 README 中鏈接到它
- [ ] 我知道文檔的位置（放在根目錄還是 docs/ 下）

---

## 🔗 文檔依賴關係

```
README.md (入口)
  │
  ├─ 引用 → DATA_FORMAT_GUIDE.md
  │          │
  │          ├─ 被 BACKEND_INTEGRATION.md 引用
  │          └─ 被前端開發者讀取
  │
  ├─ 引用 → typescript-types.ts (前端)
  │
  ├─ 引用 → BACKEND_INTEGRATION.md (後端)
  │          └─ 引用 DATA_FORMAT_GUIDE.md
  │
  ├─ 引用 → ARCHITECTURE.md (架構師)
  │          └─ 引用 DATA_FORMAT_GUIDE.md
  │
  └─ 引用 → GITHUB_SETUP.md (所有人)
```

---

## 📌 重要提醒

### 給 AI 的信息

1. **不要自作聰明創建新文檔**
   - 如果不確定，添加到現有文檔
   - 如果確實需要新文檔，在 README 中添加鏈接

2. **內容重複是可以接受的**
   - 不同角色從不同入口進來
   - 在 README 中一次，在其他文檔中再一次是 OK 的

3. **保持清晰的命名**
   - `DATA_FORMAT_GUIDE.md` ✅
   - `GUIDE.md` ❌
   - `typescript-types.ts` ✅
   - `types.md` ❌

4. **始終提供鏈接**
   - 當指向其他文檔時，使用 Markdown 鏈接
   - `[詳見 DATA_FORMAT_GUIDE.md](./docs/DATA_FORMAT_GUIDE.md)`

---

**最後更新：** 2025-11-17  
**狀態：** ✅ 完成

**注意：** 本文檔是防止 AI 和新開發者混亂的指南。如有任何不清楚的地方，請遵循本文檔。

