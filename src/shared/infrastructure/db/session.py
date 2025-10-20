from sqlalchemy.orm import Session
from .engine import SessionLocal

def get_session()-> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        