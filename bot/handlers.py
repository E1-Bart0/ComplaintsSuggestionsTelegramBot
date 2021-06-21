from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        """
        Привет!
    С моей помощью ты сможешь анонимно пожаловаться или что-нибудь предложить.
        Просто напиши мне, а я передам твое сообщение от своего имени в общую группу
    https://t.me/joinchat/dOZ_hWPNPy8wN2U6
    """
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
        text = 'Ваше сообщение отправлено в группу как "Предложение"'
        header = "😍 НОВОЕ ПРЕДЛОЖЕНИЕ 😍"
        reply_msg_to_group(update, query.message.reply_to_message, header)
    elif query.data == "complaint":
        text = 'Ваше сообщение отправлено в группу как "Жалоба"'
        header = "🤬 НОВАЯ ЖАЛОБА 🤬"
        reply_msg_to_group(update, query.message.reply_to_message, header)
    elif query.data == "anonymous message":
        text = "Ваше сообщение отправлено в группу анонимно"
        header = "😎 НОВОЕ АНОНИМНОЕ СООБЩЕНИЕ 😎"
        reply_msg_to_group(update, query.message.reply_to_message, header)
    else:
        text = "Ваше сообщение не отправлено в группу"
    query.edit_message_text(text=text)


def reply_msg_to_group(update: Update, message: Message, header):
    """Sending message to Group as a suggestion"""
    from bot.main import CHAT_ID

    message.chat.id = CHAT_ID
    update.message = message
    update.message.reply_markdown(f"**{header}**\n\n{message.text}")
