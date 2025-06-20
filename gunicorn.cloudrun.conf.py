"""Google Cloud Run用 Gunicorn設定ファイル"""

import os

# Cloud Runのポート設定
port = os.environ.get("PORT", "8080")
bind = f"0.0.0.0:{port}"

# Cloud Run最適化設定
workers = 1
threads = 8
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 0  # Cloud Runは外部でタイムアウト管理
keepalive = 2

# プロセス管理
preload_app = True
daemon = False

# ログ設定
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# セキュリティ
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Cloud Run環境変数
raw_env = [
    "APP_ENV=production",
    "DEBUG=false",
] 