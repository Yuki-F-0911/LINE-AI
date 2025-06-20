"""FastAPIアプリケーションのメインエントリーポイント"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from api.routes import webhook, health
import logging
import logging.handlers
import os
from pathlib import Path

# ログディレクトリ作成
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 本番環境用ログ設定
if settings.app_env == "production":
    # ログフォーマット
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # ファイルハンドラー（ローテーション付き）
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(getattr(logging, settings.log_level))
    
    # エラーファイルハンドラー
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setFormatter(log_format)
    error_handler.setLevel(logging.ERROR)
    
    # ルートロガー設定
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # 標準出力にも出力（Docker環境用）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(getattr(logging, settings.log_level))
    root_logger.addHandler(console_handler)
else:
    # 開発環境用ログ設定
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

# FastAPIアプリケーション初期化
app = FastAPI(
    title="LINE練習相談アプリケーション",
    description="陸上競技ランナー向けのAI練習アドバイザー",
    version="0.1.0",
    debug=settings.debug
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
app.include_router(health.router, prefix="/health", tags=["health"])

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info("LINE練習相談アプリケーションを起動しています...")
    logger.info(f"環境: {settings.app_env}")
    logger.info(f"デバッグモード: {settings.debug}")
    logger.info(f"ログレベル: {settings.log_level}")

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info("LINE練習相談アプリケーションを終了しています...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug
    ) 