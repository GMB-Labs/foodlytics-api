from sqlalchemy import Column, DateTime, Float, Integer, LargeBinary, String, ForeignKey

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(String(50), primary_key=True)
    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    nutritionist_id = Column(
        String(50),
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    gender = Column(String(10), nullable=False)
    goal_type = Column(String(50), nullable=True)
    activity_level = Column(String(20), nullable=True)
    desired_weight_kg = Column(Float, nullable=True)
    user_profile_completed = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    profile_picture_data = Column(LargeBinary, nullable=True)
    profile_picture_mime_type = Column(String(50), nullable=True)
