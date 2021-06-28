import os
from typing import Optional, Sequence, Union

from telegram import User as TelegramUser

from services.password_encrypting import generate_hash_for_password, check_password
from .core import Session
from .models import User, Config

PASSWORD = os.getenv("SU_PASSWORD", "1111")


def get_or_create_user_in_db(session: Session, user: TelegramUser) -> User:
    """Creating instance of TelegramUser in db"""
    if instance := find_user_in_db(session, user):  # noqa: ASN001
        return instance
    user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        is_bot=user.is_bot,
    )
    session.add(user)
    session.commit()
    return user


def find_user_in_db(session: Session, user: TelegramUser) -> Optional[User]:
    """Searching TelegramUser in db, returns None if not found and User if found"""
    return session.query(User).filter_by(id=user.id).first()


def delete_user_from_db(session: Session, user: TelegramUser) -> int:
    """Searching TelegramUser in db and deleting it"""
    return session.query(User).filter_by(id=user.id).delete()


def get_all_users_from_db(session: Session) -> Sequence[User]:
    """Returns all Users from db"""
    return session.query(User).all()


def get_all_superusers_from_db(session: Session) -> Sequence[User]:
    """Returns all Users with superuser permissions from db"""
    return session.query(User).filter_by(is_superuser=True).all()


def create_new_superuser_password(
    session: Session, password: Optional[str] = None
) -> Config:
    config = session.query(Config).first()
    password = password or PASSWORD
    superuser_password = generate_hash_for_password(password)

    if config:
        config.superuser_password = superuser_password
    else:
        config = Config(superuser_password=superuser_password)
        session.add(config)
    session.commit()
    return config


def check_superuser_password(session: Session, password: str) -> bool:
    hashed_password = get_or_create_su_password(session)
    return check_password(password, hashed_password)


def get_or_create_su_password(session: Session) -> str:
    config = session.query(Config).first()
    if config is None:
        config = create_new_superuser_password(session)
    return config.superuser_password


def update_to_superuser_if_password_correct(
    session: Session, password: str, telegram_user: TelegramUser
) -> Optional[bool]:
    user = get_or_create_user_in_db(session, telegram_user)
    if check_superuser_password(session, password):
        user.is_superuser = True
        session.commit()
        return True
    return False


def change_su_password_in_db(
    session: Session, telegram_user: TelegramUser, password: str
) -> Union[str, bool]:
    user = get_or_create_user_in_db(session, telegram_user)
    if user.is_superuser:
        create_new_superuser_password(session, password)
        return password
    return False
