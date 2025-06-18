"""データベース操作のテスト"""

import pytest
import pytest_asyncio
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models.user import User
from infrastructure.database.models.training_log import TrainingLog

# .envファイルの読み込み
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Windows環境での非同期テスト対応
if os.name == 'nt':  # Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# テスト用データベース接続
TEST_DATABASE_URL = os.getenv("DATABASE_URL")

@pytest_asyncio.fixture(scope="function")
async def test_session():
    """テスト用セッションフィクスチャ"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()
    await engine.dispose()

class TestDatabaseOperations:
    """データベース操作テスト"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, test_session):
        """ユーザー作成テスト"""
        # テストユーザー作成
        test_user = User(
            line_user_id="test_line_user_123",
            name="テストユーザー"
        )
        test_session.add(test_user)
        await test_session.commit()
        await test_session.refresh(test_user)
        
        # 検証
        assert test_user.id is not None
        assert test_user.line_user_id == "test_line_user_123"
        assert test_user.name == "テストユーザー"
        assert test_user.created_at is not None
        
        # クリーンアップ
        await test_session.delete(test_user)
        await test_session.commit()
    
    @pytest.mark.asyncio
    async def test_create_training_log(self, test_session):
        """練習記録作成テスト"""
        # テストユーザー作成
        test_user = User(
            line_user_id="test_line_user_456",
            name="練習テストユーザー"
        )
        test_session.add(test_user)
        await test_session.commit()
        await test_session.refresh(test_user)
        
        # 練習記録作成
        training_log = TrainingLog(
            user_id=test_user.id,
            date=datetime.now(),
            menu="ジョギング 30分",
            result="ペース 6:00/km",
            memo="体調良好"
        )
        test_session.add(training_log)
        await test_session.commit()
        await test_session.refresh(training_log)
        
        # 検証
        assert training_log.id is not None
        assert training_log.user_id == test_user.id
        assert training_log.menu == "ジョギング 30分"
        assert training_log.result == "ペース 6:00/km"
        assert training_log.memo == "体調良好"
        assert training_log.created_at is not None
        
        # クリーンアップ
        await test_session.delete(training_log)
        await test_session.delete(test_user)
        await test_session.commit()
    
    @pytest.mark.asyncio
    async def test_user_training_log_relationship(self, test_session):
        """ユーザーと練習記録の関連テスト"""
        # テストユーザー作成
        test_user = User(
            line_user_id="test_line_user_789",
            name="関連テストユーザー"
        )
        test_session.add(test_user)
        await test_session.commit()
        await test_session.refresh(test_user)
        
        # 複数の練習記録作成
        training_logs = [
            TrainingLog(
                user_id=test_user.id,
                date=datetime.now(),
                menu="ジョギング 20分",
                result="ペース 6:30/km"
            ),
            TrainingLog(
                user_id=test_user.id,
                date=datetime.now(),
                menu="インターバル走 10本",
                result="400m 1:30"
            )
        ]
        
        for log in training_logs:
            test_session.add(log)
        await test_session.commit()
        
        # ユーザーの練習記録を取得
        from sqlalchemy import select
        stmt = select(TrainingLog).where(TrainingLog.user_id == test_user.id)
        result = await test_session.execute(stmt)
        user_logs = result.scalars().all()
        
        # 検証
        assert len(user_logs) == 2
        assert user_logs[0].menu == "ジョギング 20分"
        assert user_logs[1].menu == "インターバル走 10本"
        
        # クリーンアップ
        for log in user_logs:
            await test_session.delete(log)
        await test_session.delete(test_user)
        await test_session.commit() 