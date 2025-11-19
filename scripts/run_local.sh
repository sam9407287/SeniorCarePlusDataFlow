#!/bin/bash
# 本地運行 DataFlow Pipeline

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 安裝依賴
echo "📦 安裝依賴..."
pip install -r requirements.txt

# 運行 Gateway Pipeline
echo "🚀 運行 Gateway 扁平化 Pipeline..."
python -m src.main \
  --runner DirectRunner \
  --env dev \
  --pipeline gateway \
  --input-type file \
  --input-file test_data/gateways.json \
  --output-file /tmp/gateway_flattened \
  --log-level INFO

# 運行 Anchor Pipeline
echo "🚀 運行 Anchor 扁平化 Pipeline..."
python -m src.main \
  --runner DirectRunner \
  --env dev \
  --pipeline anchor \
  --input-type file \
  --input-file test_data/anchors.json \
  --output-file /tmp/anchor_flattened \
  --log-level INFO

echo "✅ Pipeline 執行完成"
echo ""
echo "📊 輸出文件："
echo "  Gateway: /tmp/gateway_flattened*"
echo "  Anchor: /tmp/anchor_flattened*"




