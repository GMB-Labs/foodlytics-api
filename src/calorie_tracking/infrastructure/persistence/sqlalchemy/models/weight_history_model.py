from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, Date, DateTime, Float, PrimaryKeyConstraint, String

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class WeightHistoryModel(Base):
    __tablename__ = "weight_history"

    _UTC_MINUS_5 = timezone(timedelta(hours=-5))
    user_id = Column(String(50), nullable=False)
    day = Column(Date, nullable=False)
    weight_kg = Column(Float, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(WeightHistoryModel._UTC_MINUS_5),
    )

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "day", name="pk_weight_history"),
    )
