from unittest.mock import patch

from db.models import Config
from db.services import create_new_superuser_password, check_superuser_password
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
