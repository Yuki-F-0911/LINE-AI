#!/bin/bash

# LINE練習相談アプリケーション 本番環境デプロイスクリプト

set -e

echo "🚀 LINE練習相談アプリケーション デプロイ開始..."

# 環境変数確認
if [ ! -f .env ]; then
    echo "❌ .envファイルが見つかりません"
    exit 1
fi

# 依存関係インストール
echo "📦 依存関係をインストール中..."
poetry install --no-dev

# ログディレクトリ作成
echo "📁 ログディレクトリを作成中..."
mkdir -p logs

# アプリケーションユーザー作成
echo "👤 アプリケーションユーザーを作成中..."
if ! id "app" &>/dev/null; then
    sudo useradd --create-home --shell /bin/bash app
fi

# 権限設定
echo "🔐 権限を設定中..."
sudo chown -R app:app /app
sudo chmod -R 755 /app

# systemdサービス設定
echo "⚙️ systemdサービスを設定中..."
sudo cp line-running-consultation.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable line-running-consultation

# サービス起動
echo "🔄 サービスを起動中..."
sudo systemctl start line-running-consultation

# 起動確認
echo "✅ 起動状況を確認中..."
sleep 5
if sudo systemctl is-active --quiet line-running-consultation; then
    echo "✅ サービスが正常に起動しました"
else
    echo "❌ サービス起動に失敗しました"
    sudo systemctl status line-running-consultation
    exit 1
fi

# ヘルスチェック
echo "🏥 ヘルスチェックを実行中..."
if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ ヘルスチェック成功"
else
    echo "❌ ヘルスチェック失敗"
    exit 1
fi

echo "🎉 デプロイ完了！"
echo "📊 サービス状況:"
sudo systemctl status line-running-consultation --no-pager -l
echo ""
echo "📝 ログ確認:"
echo "sudo journalctl -u line-running-consultation -f"
echo ""
echo "🔄 サービス再起動:"
echo "sudo systemctl restart line-running-consultation" 