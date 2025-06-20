# LINE練習相談アプリケーション

陸上競技ランナー向けのAI練習アドバイザーLINE Botアプリケーション

## 🚀 Google Cloud Run デプロイ（推奨）

### 1. 前提条件

- Google Cloud Platform アカウント
- Google Cloud CLI インストール済み
- Docker インストール済み
- プロジェクト作成済み

### 2. 初期設定

```bash
# Google Cloud CLIログイン
gcloud auth login

# プロジェクト設定
gcloud config set project YOUR_PROJECT_ID

# 必要なAPIを有効化
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Docker認証設定
gcloud auth configure-docker
```

### 3. 環境変数（シークレット）設定

```bash
# Secret Managerにシークレットを作成
echo -n "YOUR_LINE_CHANNEL_SECRET" | gcloud secrets create line-channel-secret --data-file=-
echo -n "YOUR_LINE_CHANNEL_ACCESS_TOKEN" | gcloud secrets create line-channel-access-token --data-file=-
echo -n "YOUR_GOOGLE_API_KEY" | gcloud secrets create google-api-key --data-file=-
```

### 4. デプロイ方法

#### 手動デプロイ
```bash
# デプロイスクリプト実行
chmod +x scripts/deploy_cloudrun.sh
./scripts/deploy_cloudrun.sh
```

#### 自動デプロイ（GitHub連携）
```bash
# Cloud Build トリガー作成
gcloud builds triggers create github \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### 5. LINE Webhook URL設定

デプロイ完了後、以下のURLをLINE Developer Consoleに設定：
```
https://YOUR_SERVICE_URL/webhook/line
```

## 🚀 Render自動デプロイ設定（代替案）

### 1. Renderでの自動デプロイ設定

#### GitHubとの連携設定
1. **Renderアカウントでログイン**
   - [render.com](https://render.com)にアクセス
   - GitHubアカウントでログイン

2. **新しいサービス作成**
   - "New +" → "Blueprint"を選択
   - GitHubリポジトリを選択
   - `render.yaml`ファイルが自動検出される

3. **環境変数設定**
   ```
   LINE_CHANNEL_SECRET=your_line_channel_secret
   LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
   GOOGLE_API_KEY=your_google_api_key
   ```

4. **自動デプロイ有効化**
   - **Auto-Deploy**: `Yes`（デフォルト）
   - **Branch**: `main`
   - これでGitHubにpushするたびに自動デプロイされます

#### 自動デプロイの確認
- **デプロイ状況**: Renderダッシュボードで確認
- **ログ確認**: "Logs"タブでビルド・デプロイログを確認
- **ヘルスチェック**: `/health/`エンドポイントで自動監視

### 2. 手動デプロイが必要なケース

以下の場合のみ手動デプロイが必要：

1. **Auto-Deployを無効化している場合**
2. **環境変数を変更した場合**（一部）
3. **特定のコミットをデプロイしたい場合**
4. **ビルドが失敗して再実行したい場合**

### 3. 手動デプロイ方法

```
Renderダッシュボード → サービス選択 → "Manual Deploy"ボタン
```

### 4. デプロイ設定ファイル

- **`render.yaml`**: Renderサービス設定
- **`requirements.txt`**: Python依存関係
- **`gunicorn.conf.py`**: 本番サーバー設定

## 🚀 24時間稼働対応

### 本番環境デプロイ

#### 1. 前提条件
- Ubuntu 20.04+ / CentOS 8+
- Python 3.11+
- Poetry
- systemd対応システム

#### 2. デプロイ手順

```bash
# 依存関係インストール
poetry install --no-dev

# デプロイスクリプト実行
chmod +x scripts/deploy.sh
sudo ./scripts/deploy.sh
```

#### 3. 監視設定

```bash
# 監視スクリプトをcronに追加（5分間隔）
chmod +x scripts/monitor.sh
echo "*/5 * * * * /app/scripts/monitor.sh" | sudo crontab -
```

#### 4. サービス管理

```bash
# サービス状態確認
sudo systemctl status line-running-consultation

# サービス再起動
sudo systemctl restart line-running-consultation

# ログ確認
sudo journalctl -u line-running-consultation -f

# 自動起動有効化
sudo systemctl enable line-running-consultation
```

### Docker環境での実行

```bash
# イメージビルド
docker build -t line-running-consultation .

# コンテナ実行
docker run -d \
  --name line-running-consultation \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  line-running-consultation
```

## 📊 監視・ログ

- **ログファイル**: `logs/app.log`, `logs/error.log`
- **監視ログ**: `/var/log/line-running-consultation-monitor.log`
- **ヘルスチェック**: `http://localhost:8000/health/`

## 🔧 開発環境

```bash
# 開発サーバー起動
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 注意事項

- 本番環境では必ずHTTPSを使用してください
- 環境変数（.env）は適切に管理してください
- 定期的なバックアップを実施してください
