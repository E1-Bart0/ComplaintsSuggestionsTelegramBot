from db.models import User
from db.services import (
    delete_user_from_db,
    find_user_in_db,
    get_all_superusers_from_db,
    get_all_users_from_db,
    get_or_create_user_in_db,
)


def test_find_user_in_db__works(db_session, telegram_user):
    user = User(id=telegram_user.id, first_name=telegram_user.first_name)
    db_session.add(user)
    db_session.commit()

    result = find_user_in_db(db_session, telegram_user)
    assert result == user


def test_find_user_in_db__but_user_do_not_exists(db_session, telegram_user):
    result = find_user_in_db(db_session, telegram_user)
    assert result is None


def test_creating_user(db_session, telegram_user):
    user = get_or_create_user_in_db(db_session, telegram_user)
    all_users = db_session.query(User).all()
    assert all_users == [user]


def test_create_user__but_user_already_exists__do_not_created_user(
    db_session, telegram_user
):
    get_or_create_user_in_db(db_session, telegram_user)
    get_or_create_user_in_db(db_session, telegram_user)
    all_users = db_session.query(User).all()
    assert len(all_users) == 1


def test_get_all_users_from_db(db_session):
    user1 = User(id=1, first_name="Test user1")
    user2 = User(id=2, first_name="Test user2")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    result = get_all_users_from_db(db_session)
    assert result == [user1, user2]


def test_get_all_users_from_db__but_there_is_no_users(db_session):
    result = get_all_users_from_db(db_session)
    assert result == []


def test_get_all_users_from_db_no_mater_on_superusers(db_session):
    user1 = User(id=1, first_name="Test user1", is_superuser=True)
    user2 = User(id=2, first_name="Test user2", is_superuser=False)
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    result = get_all_users_from_db(db_session)
    assert result == [user1, user2]


def test_get_all_superusers_from_db__returns_only_superusers(db_session):
    user1 = User(id=1, first_name="Test user1", is_superuser=True)
    user2 = User(id=2, first_name="Test user2", is_superuser=False)
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    result = get_all_superusers_from_db(db_session)
    assert result == [user1]


def test_get_all_superusers_from_db__but_there_is_no_users(db_session):
    result = get_all_superusers_from_db(db_session)
    assert result == []


def test_delete_user_from_db(db_session, telegram_user):
    user = User(id=telegram_user.id, first_name=telegram_user.first_name)
    db_session.add(user)
    db_session.commit()
    result = delete_user_from_db(db_session, telegram_user)
    assert result


def test_delete_only_one_user(db_session, telegram_user):
    user = User(id=telegram_user.id, first_name=telegram_user.first_name)
    user2 = User(id=2, first_name="Test user2", is_superuser=False)
    db_session.add(user)
    db_session.add(user2)
    db_session.commit()
    all_users = db_session.query(User).all()
    assert all_users == [user, user2]

    assert delete_user_from_db(db_session, telegram_user)
    all_users = db_session.query(User).all()
    assert all_users == [user2]


def test_delete_user_from_db_but_user_do_not_exists(db_session, telegram_user):
    result = delete_user_from_db(db_session, telegram_user)
    assert not result
