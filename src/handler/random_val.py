import os
import random
from telebot import types

from utils.random_val_mode import random_from_val


def setup_random_val_handlers(bot):
    @bot.message_handler(commands=['random_val'])
    def random_val(message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row(types.KeyboardButton('Карты'))
        markup.add(types.KeyboardButton('Агенты'))
        markup.add(types.KeyboardButton('Оружия'))
        bot.send_message(message.chat.id, 'Есть 3 режима:\n1. Рандом по картам\n2. Рандом по агентам\n3. Рандом по оружиям', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)

    def on_click(message):
        if message.text == 'Карты' or message.text.strip() == '1' or message.text.strip() == '1.' or message.text.strip() == '1)':
            result = random_from_val(message.text)
            bot.send_message(message.chat.id, f'Из списка всех карт, вам выпал: <i><b>{result}</b></i>', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            file = open(f'data\\photo\\maps\\{result}.png', 'rb')
            bot.send_photo(message.chat.id, file)
        elif message.text == 'Агенты' or message.text.strip() == '2' or message.text.strip() == '2.' or message.text.strip() == '2)':
            result = random_from_val(message.text)
            count_files = os.listdir(f'data\\photo\\agents\\{result}')
            bot.send_message(message.chat.id, f'Из списка всех агентов, вам выпал(a): <i><b>{result}</b></i>', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            file = open(f'data\\photo\\agents\\{result}\\{result}_{str(random.randint(1, len(count_files)))}.png', 'rb')
            bot.send_photo(message.chat.id, file)
        elif message.text == 'Оружия' or message.text.strip() == '3' or message.text.strip() == '3.' or message.text.strip() == '3)':
            result = random_from_val(message.text)
            bot.send_message(message.chat.id, f'Из списка всех оружий, вам выпал: <i><b>{result}</b></i>', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')