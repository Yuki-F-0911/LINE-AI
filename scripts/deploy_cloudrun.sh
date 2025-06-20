#!/bin/bash

# Google Cloud Run デプロイスクリプト

set -e

# 設定
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
SERVICE_NAME="line-running-consultation"
REGION="asia-northeast1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Google Cloud Run デプロイ開始..."
echo "プロジェクト: $PROJECT_ID"
echo "サービス名: $SERVICE_NAME"
echo "リージョン: $REGION"

# 1. Dockerイメージをビルド
echo "📦 Dockerイメージをビルド中..."
docker build -f Dockerfile.cloudrun -t $IMAGE_NAME:latest .

# 2. Container Registryにプッシュ
echo "📤 Container Registryにプッシュ中..."
docker push $IMAGE_NAME:latest

# 3. Cloud Runにデプロイ
echo "🚀 Cloud Runにデプロイ中..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME:latest \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "APP_ENV=production,DEBUG=false,LOG_LEVEL=INFO" \
  --quiet

# 4. サービスURLを取得
echo "✅ デプロイ完了！"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo "🌐 サービスURL: $SERVICE_URL"
echo "🏥 ヘルスチェック: $SERVICE_URL/health/"
echo "🤖 Webhook URL: $SERVICE_URL/webhook/line"

echo ""
echo "📝 次のステップ:"
echo "1. LINE Developer ConsoleでWebhook URLを設定"
echo "2. 環境変数（シークレット）を設定"
echo "3. LINE Botでテストメッセージを送信" 