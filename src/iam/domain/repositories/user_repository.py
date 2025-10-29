from sqlalchemy import Column, String, Enum
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base
from src.iam.domain.value_objects.user_role import UserRole

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    email = Column(String, nullable=True)
