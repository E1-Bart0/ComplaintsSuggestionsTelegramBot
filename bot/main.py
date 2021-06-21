import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        """
Привет!
С моей помощью ты сможешь анонимно пожаловаться или что-нибудь предложить.
Просто напиши мне, а я передам твое сообщение от своего имени в общую группу
https://t.me/joinchat/dOZ_hWPNPy8wN2U6"""
    )


@dp.message_handler()
async def echo(message: types.Message):
    """
    This handler will be called when user sends all text messages
    """
    await message.send_copy(GROUP_ID)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
