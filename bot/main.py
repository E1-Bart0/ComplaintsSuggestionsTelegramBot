import logging
import os

from dotenv import load_dotenv
from handlers import delete_yourself_from_db, echo, help_command, parse_callback, start
from handlers_for_admin import (
    add_admins,
    add_su_user,
    get_list_of_all_admins,
    get_list_of_all_su,
    get_list_of_all_users,
    remove_admins,
    remove_su_user,
)
from handlers_for_su import alter_su_privileges, change_su_password
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

logging.basicConfig(level=logging.INFO)
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("del", delete_yourself_from_db))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # SU commands
    dispatcher.add_handler(CommandHandler("su", alter_su_privileges))
    dispatcher.add_handler(CommandHandler("new_su_password", change_su_password))

    # Admin commands
    dispatcher.add_handler(CommandHandler("all", get_list_of_all_users))
    dispatcher.add_handler(CommandHandler("all_su", get_list_of_all_su))
    dispatcher.add_handler(CommandHandler("all_admins", get_list_of_all_admins))
    dispatcher.add_handler(CommandHandler("add_su", add_su_user))
    dispatcher.add_handler(CommandHandler("add_admin", add_admins))
    dispatcher.add_handler(CommandHandler("remove_su", remove_su_user))
    dispatcher.add_handler(CommandHandler("remove_admin", remove_admins))
    dispatcher.add_handler(CallbackQueryHandler(parse_callback))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
