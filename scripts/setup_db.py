"""DB初期化スクリプト"""

import asyncio
from infrastructure.database.connection import engine, Base
from infrastructure.database.models import user, training_log

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ テーブル作成完了")

if __name__ == "__main__":
    asyncio.run(init_db()) 