"""ヘルスチェックAPI"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.config import settings
import logging

logger = logging.getLogger(__name__)

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
    logger.info("Health check endpoint accessed")
    
    response = HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="0.1.0",
        environment=settings.app_env
    )
    
    logger.info(f"Health check response: {response.status}")
    return response 