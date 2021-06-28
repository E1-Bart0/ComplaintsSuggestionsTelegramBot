from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext

from db.core import session_scope
from db.services import (
    create_user_in_db,
    delete_user_from_db,
    get_all_users_from_db,
)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    with session_scope() as session:
        create_user_in_db(session, user)
    update.message.reply_text(
        """
        Привет!
    С моей помощью ты сможешь анонимно пожаловаться или что-нибудь предложить.
        Просто напиши мне, а я передам твое сообщение всем остальным.
        Чтобы видеть сообщения других пользователей напиши мне: /su <PASSWORD>
    """
    )


def alter_su_privileges(update: Update, context: CallbackContext):
    pass


def delete_yourself(update: Update, context: CallbackContext):
    user = update.effective_user
    with session_scope() as session:
        delete_user_from_db(session, user)
    update.message.reply_text("Вы успешно удалили себя")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("HELP")


def echo(update: Update, context: CallbackContext) -> None:
    """User decides how to send his message to group: as suggestion or as complaints"""
    keyboard = [
        [
            InlineKeyboardButton("Предложение", callback_data="suggestion"),
            InlineKeyboardButton("Жалоба", callback_data="complaint"),
        ],
        [
            InlineKeyboardButton(
                "Анонимное\nСообщение", callback_data="anonymous message"
            ),
            InlineKeyboardButton("Отмена", callback_data="stop"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_id = update.message.message_id
    update.message.reply_text(
        text="Передать в группу как:",
        reply_markup=reply_markup,
        reply_to_message_id=message_id,
    )


def parse_callback(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()

    if query.data == "suggestion":
        header = "😍 НОВОЕ ПРЕДЛОЖЕНИЕ 😍"
        reply_msg_to_group(update, query.message.reply_to_message, header)
    elif query.data == "complaint":
        header = "🤬 НОВАЯ ЖАЛОБА 🤬"
        reply_msg_to_group(update, query.message.reply_to_message, header)
    elif query.data == "anonymous message":
        header = "😎 НОВОЕ АНОНИМНОЕ СООБЩЕНИЕ 😎"
        reply_msg_to_group(update, query.message.reply_to_message, header)
    query.delete_message()


def reply_msg_to_group(update: Update, message: Message, header):
    """Sending message to Group as a suggestion"""

    with session_scope() as session:
        for user in get_all_users_from_db(session):
            message.chat.id = user.id
            update.message = message

            update.message.reply_text(text=f"**{header}**\n\n{message.text}")
