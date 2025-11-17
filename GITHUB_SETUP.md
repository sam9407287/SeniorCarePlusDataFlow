# 📌 GitHub 遠端倉庫設置指南

## 步驟 1️⃣ 在 GitHub 上建立新倉庫

1. 訪問 https://github.com/new
2. 填寫以下信息：
   - **Repository name**: `SeniorCarePlusDataFlow`
   - **Description**: `Apache Beam pipeline for IoT data flattening and transformation`
   - **Visibility**: 選擇 Public 或 Private (推薦 Private)
   - **Initialize this repository with**: 取消勾選所有選項（因為我們已經有本地代碼）
3. 點擊 "Create repository"

## 步驟 2️⃣ 添加遠端倉庫

運行以下命令（將 `YOUR_USERNAME` 替換為你的 GitHub 用戶名）：

```bash
cd /Users/sam/Desktop/work/SeniorCarePlusDataFlow

# 添加遠端倉庫 - HTTPS 方式
git remote add origin https://github.com/YOUR_USERNAME/SeniorCarePlusDataFlow.git

# 或使用 SSH 方式（推薦）
git remote add origin git@github.com:YOUR_USERNAME/SeniorCarePlusDataFlow.git

# 驗證遠端配置
git remote -v
```

## 步驟 3️⃣ 推送到 GitHub

```bash
# 確保在 main 分支上
git branch -M main

# 推送所有代碼到 GitHub
git push -u origin main

# 驗證分支追蹤
git branch -vv
```

## 📊 推送完成後

你的倉庫將在以下位置可用：
- **URL**: https://github.com/YOUR_USERNAME/SeniorCarePlusDataFlow
- **Clone**: `git clone https://github.com/YOUR_USERNAME/SeniorCarePlusDataFlow.git`

## 🔐 身份驗證選項

### 選項 A：SSH （推薦）
```bash
# 生成 SSH key（如果還沒有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公鑰（複製到 GitHub Settings）
cat ~/.ssh/id_ed25519.pub

# 在 GitHub 添加 SSH key：
# Settings > SSH and GPG keys > New SSH key > 粘貼公鑰 > Add SSH key
```

### 選項 B：HTTPS + Personal Access Token
```bash
# 1. 在 GitHub 建立 Token：
#    Settings > Developer settings > Personal access tokens > Tokens (classic) > Generate new token
#    - 勾選 "repo" 作用域
#    - 複製 token

# 2. 使用 token 推送：
#    輸入用戶名時：YOUR_USERNAME
#    輸入密碼時：YOUR_PERSONAL_ACCESS_TOKEN
```

## ✅ 驗證設置

```bash
# 檢查遠端連接
git remote -v
# 應該顯示：
# origin  https://github.com/YOUR_USERNAME/SeniorCarePlusDataFlow.git (fetch)
# origin  https://github.com/YOUR_USERNAME/SeniorCarePlusDataFlow.git (push)

# 查看提交歷史
git log --oneline

# 查看當前分支
git branch -vv
```

## 🎯 後續開發工作流

### 在本地進行開發：
```bash
# 建立新分支
git checkout -b feature/your-feature

# 進行修改...

# 提交
git add .
git commit -m "feat: add your feature"

# 推送到遠端
git push origin feature/your-feature

# 在 GitHub 上建立 Pull Request
```

### 拉取最新代碼：
```bash
# 更新本地倉庫
git pull origin main
```

### 查看分支狀態：
```bash
# 查看所有分支
git branch -a

# 查看分支追蹤關係
git branch -vv
```

## 📦 完整項目結構

```
/Users/sam/Desktop/work/
├── Senior-Care-Plus/                    # 前端 (React + TypeScript)
│   └── GitHub: your-username/Senior-Care-Plus
│
├── SeniorCarePlus/                      # Android App (Kotlin)
│   └── GitHub: your-username/SeniorCarePlus
│
├── SeniorCarePlusBackend/               # 後端 (Ktor + PostgreSQL + Redis + BigQuery)
│   └── GitHub: your-username/SeniorCarePlusBackend
│
└── SeniorCarePlusDataFlow/              # 🆕 DataFlow (Python + Apache Beam)
    └── GitHub: your-username/SeniorCarePlusDataFlow
```

## 🚀 CI/CD 建議

### GitHub Actions 配置

在 `.github/workflows/` 目錄下可以配置自動化流程：

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest tests/
```

## 🆘 故障排除

### 問題：Permission denied (publickey)
**解決方案**：SSH key 未正確配置，切換到 HTTPS 或重新配置 SSH key

### 問題：fatal: could not read Username
**解決方案**：使用 Personal Access Token 而不是密碼

### 問題：Everything up-to-date
**解決方案**：正常情況，表示本地和遠端代碼一致

### 問題：branch is behind by X commits
**解決方案**：運行 `git pull origin main` 更新本地代碼

## 📚 相關文檔

- [README.md](README.md) - 項目總體說明
- [requirements.txt](requirements.txt) - Python 依賴
- [src/main.py](src/main.py) - 主入口程序

## ❓ 需要幫助？

查看 GitHub 官方文檔：
- https://docs.github.com/en/repositories/creating-and-managing-repositories
- https://docs.github.com/en/authentication

---

🎉 設置完成！你現在可以開始開發 DataFlow Pipeline 了！

