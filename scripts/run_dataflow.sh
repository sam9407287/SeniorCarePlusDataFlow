#!/bin/bash
# 在 GCP Dataflow 上運行 Pipeline

set -e

# 配置
PROJECT_ID=${1:-senior-care-plus-prod}
REGION=${2:-asia-east1}
BUCKET_NAME=${3:-senior-care-prod-temp}
ENV=${4:-prod}

echo "🚀 部署到 Google Cloud Dataflow"
echo "  項目: $PROJECT_ID"
echo "  區域: $REGION"
echo "  環境: $ENV"

# 設置 GCP 項目
gcloud config set project $PROJECT_ID

# 檢查 Bucket 是否存在
if ! gsutil ls gs://$BUCKET_NAME > /dev/null 2>&1; then
    echo "📁 建立 GCS Bucket..."
    gsutil mb -l $REGION gs://$BUCKET_NAME
fi

# 構建 Python 環境
echo "📦 準備 Python 環境..."
pip install -r requirements.txt

# 運行 Pipeline
echo "🚀 啟動 Dataflow Job..."
python -m src.main \
  --runner DataflowRunner \
  --env $ENV \
  --pipeline both \
  --input-type pubsub \
  --input-topic projects/$PROJECT_ID/topics/gateway-events \
  --output-bigquery $PROJECT_ID:senior_care_analytics.gateway_events \
  --log-level INFO

echo "✅ Dataflow Job 已提交"
echo ""
echo "📊 監控："
echo "  https://console.cloud.google.com/dataflow/jobs?project=$PROJECT_ID"

