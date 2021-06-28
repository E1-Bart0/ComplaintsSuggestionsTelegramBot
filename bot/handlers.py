from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext

from db.core import session_scope
from db.services import (
    get_or_create_user_in_db,
    delete_user_from_db,
    get_all_users_from_db,
    update_to_superuser_of_password_correct,
)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    with session_scope() as session:
        get_or_create_user_in_db(session, user)
    update.message.reply_text(
        """
        Привет!
    С моей помощью ты сможешь анонимно пожаловаться или что-нибудь предложить.
        Просто напиши мне, а я передам твое сообщение всем остальным.
        Чтобы видеть сообщения других пользователей напиши мне: /su <PASSWORD>
    """
    )


def alter_su_privileges(update: Update, context: CallbackContext):
    user = update.effective_user
    password = update.message.text[4:]
    with session_scope() as session:
        if update_to_superuser_of_password_correct(session, password, user):
            update.message.reply_text(
                "Теперь Вы Супер пользователь и можете видеть все жалобы и предложения."
                "Пожалуйста. Наслаждайтесь"
            )
        else:
            update.message.reply_text("Не корректный пароль")


def delete_yourself(update: Update, context: CallbackContext):
    user = update.effective_user
    with session_scope() as session:
        if delete_user_from_db(session, user):
            update.message.reply_text("Вы успешно удалили себя")
        else:
            update.message.reply_text(
                "Что-то пошло не так. Скорее всего Вас не было в БД"
            )


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
