from sqlalchemy.orm import Session
from typing import Generator
from .engine import SessionLocal

def get_db()-> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
