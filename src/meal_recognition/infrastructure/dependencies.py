from src.meal_recognition.infrastructure.persistence.sqlalchemy.repository.sqlalchemy_meal_repository import SqlAlchemyMealRepository
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db
from fastapi import Depends

def get_meal_repository(db = Depends(get_db)):
    return SqlAlchemyMealRepository(db)
