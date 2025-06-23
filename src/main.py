import telebot
import logging
from telebot import logger

from config.config import TOKEN

from handler.help import setup_help_handlers
from handler.other import setup_other_handlers
from handler.random_val import setup_random_val_handlers
from handler.start import setup_start_handlers
from handler.roulette import setup_roulette_handlers
from database.user import DatabaseUserCrud
from handler.info import setup_info_handlers


bot = telebot.TeleBot(TOKEN)

db = DatabaseUserCrud()

setup_start_handlers(bot=bot)
setup_roulette_handlers(bot=bot, database=db)
setup_random_val_handlers(bot=bot)
setup_info_handlers(bot=bot)
setup_help_handlers(bot=bot)
setup_other_handlers(bot=bot)

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    bot.polling(non_stop=True, skip_pending=True)