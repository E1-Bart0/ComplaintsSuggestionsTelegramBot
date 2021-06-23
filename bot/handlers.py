from collections import defaultdict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext

DATABASE = {}
MESSAGES = defaultdict(set)
M = {}


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    DATABASE[user_id] = update.message.chat.id
    update.message.reply_text(
        """
        Привет!
    С моей помощью ты сможешь анонимно пожаловаться или что-нибудь предложить.
        Просто напиши мне, а я передам твое сообщение всем остальным.
    """
    )


def delete_yourself(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    DATABASE.pop(user_id)
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
            InlineKeyboardButton("Анонимное\nСообщение", callback_data="anonymous message"),
            InlineKeyboardButton("Отмена", callback_data="stop"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_id = update.message.message_id
    update.message.reply_text(text="Передать в группу как:", reply_markup=reply_markup, reply_to_message_id=message_id)


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
    elif query.data == "like":
        upgrade_likes_on_messages(update, query.message, like=True)
        return
    elif query.data == "dislike":
        upgrade_likes_on_messages(update, query.message, like=False)
        return
    elif query.data == "none":
        return
    query.delete_message()


def upgrade_likes_on_messages(update: Update, message: Message, like: bool = True):
    msg, values = find_msg__msgs(message)
    like_or_dislike = "like" if like else "dislike"
    message_in_db = M[msg]
    message_in_db[like_or_dislike] += 1
    keyboard = [
        [
            InlineKeyboardButton(f"👍 {message_in_db['like']}", callback_data="like"),
            InlineKeyboardButton(f"👎🏿 {message_in_db['dislike']}", callback_data="dislike"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for msg in values:
        update.message = msg
        update.message.edit_reply_markup(reply_markup=reply_markup)


def find_msg__msgs(message):
    for msg, values in MESSAGES.items():
        if message in values:
            return msg, values


def reply_msg_to_group(update: Update, message: Message, header):
    """Sending message to Group as a suggestion"""
    keyboard = [
        [
            InlineKeyboardButton("👍 0", callback_data="like"),
            InlineKeyboardButton("👎🏿 0", callback_data="dislike"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    for chat in DATABASE.values():
        message.chat.id = chat
        update.message = message

        new_message = update.message.reply_text(text=f"**{header}**\n\n{message.text}", reply_markup=reply_markup)
        MESSAGES[message.message_id].add(new_message)
        M[message.message_id] = {"like": 0, "dislike": 0}
