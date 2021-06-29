from db.core import session_scope
from db.services import (
    change_su_password_in_db,
    get_or_create_user_in_db,
    update_to_superuser_if_password_correct,
)
from messages import (
    ON_CHANGE_PASSWORD_KEYBOARD_1,
    ON_CHANGE_PASSWORD_KEYBOARD_2,
    ask_about_new_password_message,
    became_su_message,
    filed_message,
    not_su_message,
    password_validation_message,
    successful_changed_password_message,
    wrong_new_password_message,
)
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


def alter_su_privileges(update: Update, context: CallbackContext):
    """Give user SU status when the command /su <password> is issued."""

    user = update.effective_user
    password = update.message.text[4:]
    with session_scope() as session:
        if update_to_superuser_if_password_correct(session, password, user):
            update.message.reply_text(became_su_message())
        else:
            update.message.reply_text(password_validation_message(password))


def change_su_password(update: Update, context: CallbackContext):
    """Change a password in DB when the command /new_su_password is issued."""
    password = update.message.text.replace("/new_su_password", "").replace(" ", "")
    if not 3 < len(password) < 17 and " " not in password and "\n" not in password:
        return update.message.reply_text(wrong_new_password_message(password))

    with session_scope() as session:
        user = get_or_create_user_in_db(session, update.effective_user)
        if user.is_superuser:
            update.message.reply_text(
                text=ask_about_new_password_message(password),
                reply_markup=InlineKeyboardMarkup(ON_CHANGE_PASSWORD_KEYBOARD_1),
            )
        else:
            update.message.reply_text(not_su_message())
    return None


def confirm_change_password(update: Update, query: Update.CALLBACK_QUERY):
    """Change SU password in db, if user confirm it"""

    password = query.message.text.split()[-1]
    with session_scope() as session:
        if change_su_password_in_db(session, update.effective_user, password):
            query.message.reply_text(
                text=successful_changed_password_message(password),
                reply_markup=InlineKeyboardMarkup(ON_CHANGE_PASSWORD_KEYBOARD_2),
            )
        else:
            query.message.reply_text(filed_message())
