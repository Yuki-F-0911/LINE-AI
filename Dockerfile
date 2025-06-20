# 本番環境用Dockerfile
FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# Poetry設定（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール
RUN poetry install --no-dev --no-interaction --no-ansi

# アプリケーションコードをコピー
COPY . .

# ログディレクトリ作成
RUN mkdir -p /app/logs

# 非rootユーザー作成
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# ポート公開
EXPOSE 8000

# 起動コマンド
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"] 