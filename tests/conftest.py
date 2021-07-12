import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from telegram import User as TelegramUser

sys.path.append(
    os.path.join(os.path.normpath(os.path.dirname(os.path.dirname(__file__))), "bot")
)

from db import models  # noqa: E402


def get_url_to_db():
    db_name = os.getenv("TEST_DB_NAME", "test")
    db_user = os.getenv("TEST_DB_USER", "test")
    db_password = os.getenv("TEST_DB_PASSWORD", "test")
    db_port = os.getenv("TEST_DB_PORT", "65433")
    db_host = os.getenv("TEST_DB_HOST", "127.0.0.1")
    db_type = os.getenv("TEST_DB_TYPE", "postgresql")
    return f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


@pytest.fixture(scope="session")
def connection():
    engine = create_engine(get_url_to_db())
    return engine.connect()


@pytest.fixture(scope="session")
def _setup_database(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()
    yield
    models.Base.metadata.drop_all()


@pytest.fixture()
def db_session(_setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


@pytest.fixture()
def telegram_user():
    user_info = {
        "is_bot": False,
        "id": 1111,
        "first_name": "John",
        "last_name": "Doe",
        "language_code": "en",
        "username": "python_test",
    }
    return TelegramUser(**user_info)
