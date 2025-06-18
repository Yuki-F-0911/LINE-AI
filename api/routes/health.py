"""ヘルスチェックAPI"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str
    timestamp: datetime
    version: str
    environment: str


@router.get("/", response_model=HealthResponse)
async def health_check():
    """ヘルスチェック"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="0.1.0",
        environment=settings.app_env
    ) 