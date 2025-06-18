"""アプリケーション設定管理"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # LINE Bot Settings
    line_channel_secret: str
    line_channel_access_token: str
    
    # Google Gemini API
    google_api_key: str
    
    # Database Settings
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    
    # Application Settings
    app_env: str = "development"
    debug: bool = True
    secret_key: str
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# グローバル設定インスタンス
settings = Settings() 