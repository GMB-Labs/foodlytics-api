from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.shared.infrastructure.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)
Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)