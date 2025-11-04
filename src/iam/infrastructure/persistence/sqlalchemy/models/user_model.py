from sqlalchemy import Column, String, Index
from sqlalchemy.types import JSON
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # auth0 sub
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=True, unique=True, index=True)

    role = Column(String, nullable=False, default="PATIENT")

    scopes = Column(JSON, nullable=False, default=list)
    permissions = Column(JSON, nullable=False, default=list)
