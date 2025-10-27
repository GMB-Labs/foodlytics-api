from sqlalchemy.orm import Session
from src.iam.domain.repositories.user_repository import UserRepository
from src.iam.domain.aggregates.user import User

class UserRepositoryImpl(UserRepository):
    def __init__(self,session:Session):
        self.session = session

    def add_user(self,user:User) -> None:
        self.session.add(user)

    def get_all_users(self):
        return self.session.query(User).all()