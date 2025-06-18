"""環境変数ファイル作成スクリプト"""

env_content = """# LINE Bot Settings
LINE_CHANNEL_SECRET=e22c3692c4d8d565608d26cf127d849c
LINE_CHANNEL_ACCESS_TOKEN=7E9ThPK/XsQAXHC0WtxBucPEQcYpX6IKZyaqO+vbdvac1ownOw4ACn9TRnNOQOveFOouXrvPf+LFBlZJx4zrL5sUWUX5939HY2UEKRc0j/0EK9nee6SxAeSnB6jigaJqipUtC0cJW4HBpMIdlKzfkgdB04t89/1O/w1cDnyilFU=

# Google Gemini API
GOOGLE_API_KEY=AIzaSyADaWhkISci9lrtrDKN97XkO6eu0tiSBUc

# Database Settings
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/line_running_db
REDIS_URL=redis://localhost:6379/0

# Application Settings
APP_ENV=development
DEBUG=true
SECRET_KEY=test_secret_key_for_development_only

# Logging
LOG_LEVEL=INFO
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("環境変数ファイル .env を更新しました") 