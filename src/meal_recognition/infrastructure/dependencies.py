'''
from src.meal_recognition.infrastructure.persistence.sqlalchemy.repository.sqlalchemy_meal_repository import SqlAlchemyMealRepository

from src.shared.infrastructure.persistence.sqlalchemy.session import get_session_factory


def get_meal_repository():
    return SqlAlchemyMealRepository(get_session_factory)
'''