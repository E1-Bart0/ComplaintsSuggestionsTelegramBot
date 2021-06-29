from typing import Callable, Sequence

from db.core import session_scope
from db.models import User
from db.services import (
    get_all_admins_from_db,
    get_all_non_admins_from_db,
    get_all_non_su_from_db,
    get_all_superusers_from_db,
    get_all_users_from_db,
    get_or_create_user_in_db,
    set_remove_status_from_user,
)
from messages import (
    ALL_ADMIN_HEADER,
    ALL_SU_HEADER,
    ALL_USERS_HEADER,
    add_to_admin_message,
    add_to_su_message,
    became_admin_message,
    became_non_admin_message,
    became_non_su_message,
    became_su_message,
    filed_message,
    get_all_members_message,
    get_username,
    not_members_message,
    remove_from_admin_message,
    remove_from_su_message,
    user_became_admin_message,
    user_became_not_admin_message,
    user_became_not_su_message,
    user_became_su_message,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


def get_list_of_all_users(update: Update, context: CallbackContext):
    """Get All users from DB when the command /all is issued."""
    get_all(update, get_all_users_from_db, ALL_USERS_HEADER)


def get_list_of_all_su(update: Update, context: CallbackContext):
    """Get All users with SU privileges from DB when the command /all_su is issued."""
    get_all(update, get_all_superusers_from_db, ALL_SU_HEADER)


def get_list_of_all_admins(update: Update, context: CallbackContext):
    """Get All users with admin privileges from DB when the command /all_admins is issued."""
    get_all(update, get_all_admins_from_db, ALL_ADMIN_HEADER)


def get_all(update, users_from_db: Callable, header: str):
    """Get users  from DB by function (users_from_db)"""
    telegram_user = update.effective_user
    with session_scope() as session:
        user = get_or_create_user_in_db(session, telegram_user)
        if user.is_admin:
            members = users_from_db(session)
            if members:
                update.message.reply_text(get_all_members_message(members, header))
            else:
                update.message.reply_text(not_members_message())


def add_su_user(update: Update, context: CallbackContext):
    """Add SU status to User when the command /add_su is issued."""
    add_remove_user_status(
        update, get_all_non_su_from_db, add_to_su_message, "Добавить", "add_su"
    )


def add_admins(update: Update, context: CallbackContext):
    """Add admin status to user when the command /add_admin is issued."""
    add_remove_user_status(
        update,
        get_all_non_admins_from_db,
        add_to_admin_message,
        "Добавить",
        "add_admin",
    )


def remove_su_user(update: Update, context: CallbackContext):
    """Remove SU status from User when the command /remove_su is issued."""
    add_remove_user_status(
        update,
        get_all_superusers_from_db,
        remove_from_su_message,
        "Удалить",
        "remove_su",
    )


def remove_admins(update: Update, context: CallbackContext):
    """Remove Admin status from user when the command /remove_admin is issued."""
    add_remove_user_status(
        update,
        get_all_admins_from_db,
        remove_from_admin_message,
        "Удалить",
        "remove_admin",
    )


def add_remove_user_status(
    update: Update,
    get_all_users: Callable,
    text_message: Callable,
    add_remove: str,
    callback_text: str,
):
    """Get All Users and Ask Admin whom we wants to upgrade(is_admin, is_superuser)"""
    telegram_user = update.effective_user
    with session_scope() as session:
        user = get_or_create_user_in_db(session, telegram_user)
        if user.is_admin:
            all_user = get_all_users(session)
            update.message.reply_text(text_message())
            if not all_user:
                return update.message.reply_text(not_members_message())
            return send_msg_with_user_and_keyboard(
                update, all_user, add_remove, callback_text
            )
        return None


def send_msg_with_user_and_keyboard(
    update: Update, all_user: Sequence[User], keyboard_text, callback
):
    """Get All Users and send them to User"""
    for user in all_user:
        keyboard = [
            [
                InlineKeyboardButton(
                    keyboard_text, callback_data=f"{callback} {user.id}"
                )
            ],
        ]
        update.message.reply_text(
            text=get_username(user),
            reply_markup=InlineKeyboardMarkup(keyboard),
            timeout=10,
        )


def add_user_to_su_group(query: Update.CALLBACK_QUERY, user_id: str):
    """Add User SU status"""
    get_user_and_change_his_status(
        query, user_id, "is_superuser", True, user_became_su_message, became_su_message
    )


def remove_user_from_su_group(query: Update.CALLBACK_QUERY, user_id: str):
    """Remove from User SU status"""
    get_user_and_change_his_status(
        query,
        user_id,
        "is_superuser",
        False,
        user_became_not_su_message,
        became_non_su_message,
    )


def add_user_to_admin_group(query: Update.CALLBACK_QUERY, user_id: str):
    """Add User admin status"""
    get_user_and_change_his_status(
        query,
        user_id,
        "is_admin",
        True,
        user_became_admin_message,
        became_admin_message,
    )


def remove_user_from_admin_group(query: Update.CALLBACK_QUERY, user_id: str):
    """Remove from User admin status"""
    get_user_and_change_his_status(
        query,
        user_id,
        "is_admin",
        False,
        user_became_not_admin_message,
        became_non_admin_message,
    )


def get_user_and_change_his_status(
    query: Update.CALLBACK_QUERY,
    user_id: str,
    status: "str",
    new_status: bool,
    on_success_msg: Callable,
    send_to_user_msg: Callable,
):
    """Find User in DB and Change his status"""
    user_id = int(user_id.split()[1])
    with session_scope() as session:
        user_or_none = set_remove_status_from_user(session, user_id, status, new_status)
        if user_or_none:
            query.message.reply_text(on_success_msg(user_or_none))
            send_msg_to_user(query, user_or_none, send_to_user_msg)
        else:
            query.message.reply_text(filed_message())


def send_msg_to_user(query: Update.CALLBACK_QUERY, user: User, msg: Callable):
    """Send notification to User about his new status"""
    id_before_change = query.message.chat.id
    query.message.chat.id = user.id
    query.message.reply_text(msg())
    query.message.chat.id = id_before_change
