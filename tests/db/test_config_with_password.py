from unittest.mock import patch

from db.models import Config, User
from db.services import (
    create_new_superuser_password,
    check_superuser_password,
    update_to_superuser_of_password_correct,
    get_or_create_user_in_db,
)
from services.password_encrypting import generate_hash_for_password, check_password


def test_generate_hash_for_password():
    key_word = "1111"
    hashed = generate_hash_for_password(key_word)
    assert len(hashed) == 60


def test_check_password__return_true():
    key_word = "1111"
    hashed = generate_hash_for_password(key_word)
    assert check_password(key_word, hashed)


def test_check_password__return_false_wrong_password():
    key_word = "1111"
    hashed = generate_hash_for_password(key_word)
    assert not check_password("2111", hashed)


def test_create_new_superuser_password_if_config_do_not_exists(db_session):
    config = create_new_superuser_password(db_session)
    configs = db_session.query(Config).all()
    assert configs == [config]
    assert len(config.superuser_password) == 60


def test_create_new_superuser_password_if_config_already_exists(db_session):
    config = Config(superuser_password="111")  # noqa: S106
    db_session.add(config)
    db_session.commit()

    config = create_new_superuser_password(db_session)
    configs = db_session.query(Config).all()
    assert configs == [config]
    assert len(config.superuser_password) == 60


def test_check_superuser_password__if_not_config__password_not_correct(db_session):
    result = check_superuser_password(db_session, "not_correct")
    assert not result


@patch("db.services.PASSWORD", "correct")
def test_check_superuser_password__if_not_config__password_correct(db_session):
    result = check_superuser_password(db_session, "correct")
    assert result


@patch("db.services.check_password", return_value=True)
def test_check_superuser_password__if_config_exists(mock, db_session):
    create_new_superuser_password(db_session)
    result = check_superuser_password(db_session, "correct")
    assert result


@patch("db.services.check_password", return_value=True)
def test_update_to_superuser_of_password_correct__password_correct(
    mock, db_session, telegram_user
):
    get_or_create_user_in_db(db_session, telegram_user)
    result = update_to_superuser_of_password_correct(
        db_session, "correct", telegram_user
    )
    assert result
    user = db_session.query(User).first()
    assert user.is_superuser


@patch("db.services.check_password", return_value=False)
def test_update_to_superuser_of_password_correct__password_not_correct(
    mock, db_session, telegram_user
):
    get_or_create_user_in_db(db_session, telegram_user)
    result = update_to_superuser_of_password_correct(
        db_session, "in_correct", telegram_user
    )
    assert not result
    user = db_session.query(User).first()
    assert not user.is_superuser


@patch("db.services.check_password", return_value=True)
def test_update_to_superuser_of_password_correct__if_not_user_in_db_but_password_correct(
    mock, db_session, telegram_user
):
    result = update_to_superuser_of_password_correct(
        db_session, "correct", telegram_user
    )
    assert result
    user = db_session.query(User).first()
    assert user.is_superuser


@patch("db.services.check_password", return_value=False)
def test_update_to_superuser_of_password_correct__if_not_user_in_db_but_password_incorrect(
    mock, db_session, telegram_user
):
    result = update_to_superuser_of_password_correct(
        db_session, "in_correct", telegram_user
    )
    assert not result
    user = db_session.query(User).first()
    assert not user.is_superuser
