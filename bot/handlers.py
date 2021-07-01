from db.core import session_scope
from db.services import (
    create_user_as_admin_if_no_more_users_in_db,
    delete_user_from_db,
    get_all_superusers_from_db,
    get_or_create_user_in_db,
)
from handlers_for_admin import (
    add_user_to_admin_group,
    add_user_to_su_group,
    remove_user_from_admin_group,
    remove_user_from_su_group,
)
from handlers_for_su import confirm_change_password
from messages import (
    ANONYMOUS_MSG_HEADER,
    COMPLAINT_HEADER,
    NEW_PASSWORD_HEADER,
    ON_COMPLAINT_SUGGESTION_KEYBOARD,
    SUGGESTION_HEADER,
    ask_how_to_transfer_message,
    combine_header_and_msg,
    help_message,
    on_delete_message,
    on_failed_deleted_message,
    start_message,
    you_send_anonymous_message,
    you_send_complaint_message,
    you_send_suggestion_message,
    you_success_send_message,
)
from telegram import InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    with session_scope() as session:
        create_user_as_admin_if_no_more_users_in_db(session, user)
    update.message.reply_text(start_message(user.full_name))


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
    with session_scope() as session:
        user = get_or_create_user_in_db(session, update.effective_user)
        update.message.reply_text(help_message(user))


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


def parse_callback(update: Update, context: CallbackContext) -> None:  # noqa: CCR001
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()

    if query.data == "suggestion":
        reply_msg_to_group(
            update,
            query.message.reply_to_message,
            SUGGESTION_HEADER,
            you_send_suggestion_message(),
        )
    elif query.data == "complaint":
        reply_msg_to_group(
            update,
            query.message.reply_to_message,
            COMPLAINT_HEADER,
            you_send_complaint_message(),
        )
    elif query.data == "anonymous message":
        reply_msg_to_group(
            update,
            query.message.reply_to_message,
            ANONYMOUS_MSG_HEADER,
            you_send_anonymous_message(),
        )
    elif query.data == "confirm_change_password":
        confirm_change_password(update, query)
    elif query.data == "info_about_changing":
        reply_msg_to_group(
            update, query.message, NEW_PASSWORD_HEADER, you_success_send_message()
        )
    elif "add_su" in query.data:
        add_user_to_su_group(query, query.data)
    elif "add_admin" in query.data:
        add_user_to_admin_group(query, query.data)
    elif "remove_su" in query.data:
        remove_user_from_su_group(query, query.data)
    elif "remove_admin" in query.data:
        remove_user_from_admin_group(query, query.data)
    elif query.data == "pass":
        pass
    query.delete_message()


def reply_msg_to_group(
    update: Update, message: Message, header: str, success_text: str
):
    """Sending message to all SuperUser"""
    main_chat_id = message.chat.id
    with session_scope() as session:
        for user in get_all_superusers_from_db(session):
            message.chat.id = user.id
            update.message = message
            update.message.reply_text(combine_header_and_msg(header, message))

    update.message = message
    update.message.chat.id = main_chat_id
    update.message.reply_text(success_text)
