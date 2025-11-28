from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Index

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class NutritionistInviteCodeModel(Base):
    __tablename__ = "nutritionist_invite_codes"

    _UTC_MINUS_5 = timezone(timedelta(hours=-5))
    code = Column(String(6), primary_key=True)
    nutritionist_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    patient_id = Column(String(50), ForeignKey("users.id"), nullable=True, index=True)
    used = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(NutritionistInviteCodeModel._UTC_MINUS_5)
    )
    used_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (Index("ix_nic_used", "used"),)
