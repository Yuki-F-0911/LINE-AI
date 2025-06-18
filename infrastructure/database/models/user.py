"""ユーザーモデル"""

import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from infrastructure.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    line_user_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) 