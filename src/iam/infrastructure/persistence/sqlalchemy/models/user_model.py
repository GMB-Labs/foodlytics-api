from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base

try:
    JsonType = JSONB
except Exception:
    JsonType = JSON


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True, index=True)

    role = Column(String, nullable=False)

    #Lists
    scopes = Column(JsonType, nullable=False, default=list)
    permissions = Column(JsonType, nullable=False, default=list)