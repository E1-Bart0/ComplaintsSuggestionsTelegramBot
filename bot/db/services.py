from telegram import User as TelegramUser

from .core import Session
from .models import User


def create_user_in_db(session: Session, user: TelegramUser):
    User(id=user.id)


def find_user_in_db(session: Session, user_id: int):
    pass


def delete_user_from_db(session: Session, user: TelegramUser):
    pass


def get_all_users_from_db(session: Session):
    pass
