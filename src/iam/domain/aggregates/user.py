from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    # ID local (clave primaria de tu sistema)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # ID de Auth0 (clave externa única, el 'sub')
    auth0_id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, auth0_id: str, email: str, name: str = None):
        self.auth0_id = auth0_id
        self.email = email
        self.name = name

    def __repr__(self):
        return f"<User(id={self.id}, auth0_id='{self.auth0_id}', email='{self.email}')>"