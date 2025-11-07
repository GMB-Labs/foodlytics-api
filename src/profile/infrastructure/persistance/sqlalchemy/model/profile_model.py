from sqlalchemy import Column, DateTime, Float, Integer, LargeBinary, String

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False, unique=True, index=True)
    nutritionist_id = Column(String(50), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    gender = Column(String(10), nullable=False)
    goal_type = Column(String(50), nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    profile_picture_data = Column(LargeBinary, nullable=True)
    profile_picture_mime_type = Column(String(50), nullable=True)
