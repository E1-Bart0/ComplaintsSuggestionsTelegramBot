from db.core import session_scope
from db.services import (
    change_su_password_in_db,
    delete_user_from_db,
    get_all_superusers_from_db,
    get_or_create_user_in_db,
    update_to_superuser_if_password_correct,
)
from messages import (
    ANONYMOUS_MSG_HEADER,
    COMPLAINT_HEADER,
    NEW_PASSWORD_HEADER,
    ON_CHANGE_PASSWORD_KEYBOARD_1,
    ON_CHANGE_PASSWORD_KEYBOARD_2,
    ON_COMPLAINT_SUGGESTION_KEYBOARD,
    SUGGESTION_HEADER,
    ask_about_new_password_message,
    ask_how_to_transfer_message,
    became_su_message,
    combine_header_and_msg,
    filed_change_password_message,
    help_message,
    not_su_message,
    on_delete_message,
    on_failed_deleted_message,
    password_validation_message,
    start_message,
    successful_changed_password_message,
    wrong_new_password_message,
)
from telegram import InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    with session_scope() as session:
        get_or_create_user_in_db(session, user)
    update.message.reply_text(start_message(user.full_name))


def alter_su_privileges(update: Update, context: CallbackContext):
    user = update.effective_user
    password = update.message.text[4:]
    with session_scope() as session:
        if update_to_superuser_if_password_correct(session, password, user):
            update.message.reply_text(became_su_message())
        else:
            update.message.reply_text(password_validation_message(password))


def change_su_password(update: Update, context: CallbackContext):
    """Change a password in DB when the command /new_su_password is issued."""
    telegram_user = update.effective_user
    password = update.message.text.replace("/new_su_password", "").replace(" ", "")
    if not 3 < len(password) < 17 and " " not in password and "\n" not in password:
        return update.message.reply_text(wrong_new_password_message(password))

    with session_scope() as session:
        user = get_or_create_user_in_db(session, telegram_user)
        if user.is_superuser:
            update.message.reply_text(
                text=ask_about_new_password_message(password),
                reply_markup=InlineKeyboardMarkup(ON_CHANGE_PASSWORD_KEYBOARD_1),
            )
        else:
            update.message.reply_text(not_su_message())
    return None


def delete_yourself_from_db(update: Update, context: CallbackContext):
    """Delete a user from DB when the command /del is issued."""
    user = update.effective_user
    with session_scope() as session:
        if delete_user_from_db(session, user):
            update.message.reply_text(on_delete_message())
        else:
            update.message.reply_text(on_failed_deleted_message())


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_message())


def echo(update: Update, context: CallbackContext) -> None:
    """User decides how to send his message to group: as suggestion or as complaints"""
    message_id = update.message.message_id
    with session_scope() as session:
        get_or_create_user_in_db(session, update.effective_user)

    update.message.reply_text(
        text=ask_how_to_transfer_message(),
        reply_markup=InlineKeyboardMarkup(ON_COMPLAINT_SUGGESTION_KEYBOARD),
        reply_to_message_id=message_id,
    )


def parse_callback(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()

    if query.data == "suggestion":
        reply_msg_to_group(update, query.message.reply_to_message, SUGGESTION_HEADER)
    elif query.data == "complaint":
        reply_msg_to_group(update, query.message.reply_to_message, COMPLAINT_HEADER)
    elif query.data == "anonymous message":
        reply_msg_to_group(update, query.message.reply_to_message, ANONYMOUS_MSG_HEADER)
    elif query.data == "confirm_change_password":
        confirm_change_password(update, query)
    elif query.data == "info_about_changing":
        reply_msg_to_group(update, query.message, NEW_PASSWORD_HEADER)
    elif query.data == "pass":
        pass
    query.delete_message()


def confirm_change_password(update: Update, query: Update.CALLBACK_QUERY):
    telegram_user = update.effective_user
    password = query.message.text.split()[-1]
    with session_scope() as session:
        if change_su_password_in_db(session, telegram_user, password):
            query.message.reply_text(
                text=successful_changed_password_message(password),
                reply_markup=InlineKeyboardMarkup(ON_CHANGE_PASSWORD_KEYBOARD_2),
            )
        else:
            query.message.reply_text(filed_change_password_message())


def reply_msg_to_group(update: Update, message: Message, header):
    """Sending message to all SuperUser"""

    with session_scope() as session:
        for user in get_all_superusers_from_db(session):
            message.chat.id = user.id
            update.message = message
            update.message.reply_text(combine_header_and_msg(header, message))
