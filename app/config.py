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
    
    # Database Settings (Optional for now)
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    
    # Application Settings
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "default_secret_key"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# グローバル設定インスタンス
settings = Settings() 