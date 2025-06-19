"""FastAPIアプリケーションのメインエントリーポイント"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from api.routes import webhook, health
import logging
import os

# ログ設定
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

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info("アプリケーションを終了しています...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug
    ) 