import os
import telebot
import random
import logging
from telebot import types, logger
from config.configToken import TOKEN
from module.other.checkFromat import check
from module.other.map_pool import random_from_val
from module.other.roulette_casino import game_rulette_casino
from module.funcBD.func_on_db import updataBalance, createdDB, add_user_db, get_user_db

bot = telebot.TeleBot(TOKEN)
casino_mode = None
stavka = None
balance = 0

createdDB()

# Обработка /start
@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Поиграть со мной', callback_data='game')
    markup.row(btn1)
    markup.add(types.InlineKeyboardButton('Поболтать со мной', callback_data='chating'))
    markup.add(types.InlineKeyboardButton('Наш дискорд сервер))', url='https://discord.com/invite/tTQJMrXyPw'))
    bot.send_message(message.chat.id, 'Ку, интересно что я могу? Потыкай кнопки и узнаешь)', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'game':
        bot.send_message(callback.message.chat.id, 'Есть несколько игр, а именно:\n1. Рандомайзер Для Валоранта (/random_val)\n2. Казино: Рулетка (/roulette)')
    elif callback.data == 'chating':
        bot.send_message(callback.message.chat.id, 'Ну лан, давай попиздим, что как ты?')


# Обработка /random_val
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
        file = open(f'data/photo/maps/{result}.png', 'rb')
        bot.send_photo(message.chat.id, file)
    elif message.text == 'Агенты' or message.text.strip() == '2' or message.text.strip() == '2.' or message.text.strip() == '2)':
        result = random_from_val(message.text)
        count_files = os.listdir(f'data/photo/agents/{result}')
        bot.send_message(message.chat.id, f'Из списка всех агентов, вам выпал(a): <i><b>{result}</b></i>', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        file = open(f'data/photo/agents/{result}/{result}_{str(random.randint(1, len(count_files)))}.png', 'rb')
        bot.send_photo(message.chat.id, file)
    elif message.text == 'Оружия' or message.text.strip() == '3' or message.text.strip() == '3.' or message.text.strip() == '3)':
        result = random_from_val(message.text)
        bot.send_message(message.chat.id, f'Из списка всех оржий, вам выпал: <i><b>{result}</b></i>', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')


# Обработка /roulette
@bot.message_handler(commands=['roulette'])
def roulette_cas(message):    
    add_user_db(message.from_user.id, message.from_user.username)
    
    if message.text == '/roulette' or message.text == 'Да, давай' or message.text.lower() == 'да' or message.text.lower() == '+' or message.text.lower() == 'yes':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row(types.KeyboardButton('👔 Мой профиль'))
        markup.row(types.KeyboardButton('Красное или Черное'), types.KeyboardButton('Нечетное или четное'))
        markup.row(types.KeyboardButton('Ставка на конкретное число'))
        markup.row(types.KeyboardButton('Ставка «Малые и большие номера»'), types.KeyboardButton('Дюжины'))
        bot.send_message(message.chat.id, 'Отлично! Значит хотим испытать удачу🍀?)\nНапоминаю правила игры, вы выбераете, как вы будете ставить, ставите и надеетесь на удачу!\nBceго 5 видов:\n1. На красное или черное\n2. Нечетное или четное\n3. Ставка на конкретное число\n4. Ставка «Малые и большие номера»\n5. Дюжины', reply_markup=markup)
        bot.register_next_step_handler(message, next_roulette)
    else:
        bot.send_message(message.chat.id, 'Ну и не надо', reply_markup=types.ReplyKeyboardRemove())

def next_roulette(message):
    if message.text == "👔 Мой профиль":
        profile(message)
    elif message.text == 'Красное или Черное' or message.text.strip() == '1' or message.text.strip() == '1.' or message.text.strip() == '1)':
        bot.send_message(message.chat.id, 'Хочу напомнить, в этом типе ставки ты можешь выбрать:\n🔴Красное🔴 или ⚫Черное⚫', reply_markup=types.ReplyKeyboardRemove())
        markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup1.row(types.KeyboardButton('🔴Красное🔴'), types.KeyboardButton('⚫Черное⚫'))
        bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
        bot.register_next_step_handler(message, next_roulette_rate)
    elif message.text == 'Нечетное или четное' or message.text.strip() == '2' or message.text.strip() == '2.' or message.text.strip() == '2)':
        bot.send_message(message.chat.id, 'Хочу напомнить, в этом типе ставки ты можешь выбрать:\nЧетное или Нечетное', reply_markup=types.ReplyKeyboardRemove())
        markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup1.row(types.KeyboardButton('Четное'), types.KeyboardButton('Нечетное'))
        bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
        bot.register_next_step_handler(message, next_roulette_rate)
    elif message.text == 'Ставка на конкретное число' or message.text.strip() == '3' or message.text.strip() == '3.' or message.text.strip() == '3)':
        bot.send_message(message.chat.id, 'Хочу напомнить, в этом типе ставки ты можешь выбрать число от 0 до 36\nДля ставки просто напишите число в чат', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, next_roulette_rate)
    elif message.text == 'Ставка «Малые и большие номера»' or message.text.strip() == '4' or message.text.strip() == '4.' or message.text.strip() == '4)':
        bot.send_message(message.chat.id, 'Хочу напомнить правила, в этом типе ставки ты можешь выбрать:\n1. Малые числа (от 1 до 18)\n2. Большие числа (от 19 до 36)', reply_markup=types.ReplyKeyboardRemove())
        markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup1.row(types.KeyboardButton('Малые числа'), types.KeyboardButton('Большие числа'))
        bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
        bot.register_next_step_handler(message, next_roulette_rate)
    elif message.text == 'Дюжины' or message.text.strip() == '5' or message.text.strip() == '5.' or message.text.strip() == '5)':
        bot.send_message(message.chat.id, 'Хочу напомнить правила, в этом типе ставки ты можешь выбрать одну из 3 дюжин:\n1. Первая дюжина — числа от 1 до 12\n2. Вторая дюжина — числа от 13 до 24\n3. Третья дюжина — числа от 25 до 36', reply_markup=types.ReplyKeyboardRemove())
        markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup1.row(types.KeyboardButton('Первая дюжина'))
        markup1.row(types.KeyboardButton('Вторая дюжина'))
        markup1.row(types.KeyboardButton('Третья дюжина'))
        bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
        bot.register_next_step_handler(message, next_roulette_rate)

# Вывод данных профиля игрока
def profile(message):
    user = get_user_db(message.from_user.id)
    bot.send_message(message.chat.id, f"Игрок: {user[0][3]}\nБаланс: {user[0][2]}💰")
    bot.send_message(message.chat.id, "Не заубдьте выбрать один из режимов игры:\n1. На красное или черное\n2. Нечетное или четное\n3. Ставка на конкретное число\n4. Ставка «Малые и большие номера»\n5. Дюжины")
    bot.register_next_step_handler(message, next_roulette)

def next_roulette_rate(message):
    global casino_mode
    global balance
    casino_mode = message.text # Сохранили на что ставим (красное, черное, число, первая дюжина и т.д.)
    user = get_user_db(message.from_user.id)
    balance = user[0][2]
    bot.send_message(message.chat.id, f"Какую сумму хотите поставить (напишите в чат)?\nВаш баланс: {balance}💰")
    
    if casino_mode == "🔴Красное🔴" or casino_mode.lower() == "красное" or casino_mode.lower() == "к" or casino_mode == '⚫Черное⚫' or casino_mode.lower() == "черное" or casino_mode.lower() == "чёрное" or casino_mode.lower() == "ч":
        bot.register_next_step_handler(message, next_roulette_rb)
    elif casino_mode == 'Четное' or casino_mode == 'Нечетное':
        bot.register_next_step_handler(message, next_roulette_dch)
    elif casino_mode == 'Малые числа' or casino_mode == 'Большие числа':
        bot.register_next_step_handler(message, next_roulette_mb)
    elif casino_mode == 'Первая дюжина' or casino_mode == 'Вторая дюжина' or casino_mode == 'Третья дюжина':
        bot.register_next_step_handler(message, next_roulette_du)
    elif casino_mode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']:
        bot.register_next_step_handler(message, next_roulette_number)

# Рулетка: Красное-Черное
def next_roulette_rb(message):
    global casino_mode
    global stavka
    global balance
    try:
        stavka = int(message.text)
        if check(stavka, balance) == False:
            bot.send_message(message.chat.id, 'Вы ввели некоректное значение.\nОтмена операции.')
        else:
            balance -= stavka
            result = game_rulette_casino()
            bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            if casino_mode == "🔴Красное🔴" or casino_mode.lower() == "красное" or casino_mode.lower() == "к":
                if result[1] == '🔴':
                    balance += stavka * 2
                    bot.send_message(message.chat.id, f'Повезло, поршивец!\nДействие: +{stavka}💵\nТвой баланс: {balance}💰')
                elif result[1] == '⚫' or result[1] == '🟢':
                    bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            elif casino_mode == '⚫Черное⚫' or casino_mode.lower() == "черное" or casino_mode.lower() == "чёрное" or casino_mode.lower() == "ч":
                if result[1] == '🔴':
                    bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
                elif result[1] == '⚫' or result[1] == '🟢':
                    balance += stavka * 2
                    bot.send_message(message.chat.id, f'Повезло, поршивец!\nДействие: +{stavka}💵\nТвой баланс: {balance}💰')
        
            # Обновление данных balance для пользователя
            updataBalance(balance, message.from_user.id)
        
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
            bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
            bot.register_next_step_handler(message, roulette_cas)
    except:
        bot.send_message(message.chat.id, 'Вы ввели некоректное значение.\nОтмена операции.')

# Рулетка: Четные-Нечетные
def next_roulette_dch(message):
    global casino_mode
    global stavka
    global balance
    try:
        stavka = int(message.text)
        if check(stavka, balance) == False:
            bot.send_message(message.chat.id, 'Вы ввели некоректное значение.\nОтмена операции.')
        else:
            balance -= stavka
            result = game_rulette_casino()
            bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            if casino_mode == 'Четное':
                if result[0] % 2 == 0:
                    balance += stavka * 2
                    bot.send_message(message.chat.id, f'Повезло, поршивец!\nДействие: +{stavka}💵\nТвой баланс: {balance}💰')
                elif result[0] % 2 != 0 or result[0] == 0:
                    bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            elif casino_mode == 'Нечетное':
                if result[0] % 2 == 0 or result[0] == 0:
                    bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
                elif result[0] % 2 != 0:
                    balance += stavka * 2
                    bot.send_message(message.chat.id, f'Повезло, поршивец!\nДействие: +{stavka}💵\nТвой баланс: {balance}💰')
        
            # Обновление данных balance для пользователя
            updataBalance(balance, message.from_user.id)
        
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
            bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
            bot.register_next_step_handler(message, roulette_cas)
    except:
        bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')

# Рулекта: Конкретное число
def next_roulette_number(message):
    global casino_mode
    global stavka
    global balance
    try:
        stavka = int(message.text)
        if check(stavka, balance) == False:
            bot.send_message(message.chat.id, 'Вы ввели некоректное значение.\nОтмена операции.')
        else:
            balance -= stavka
            result = game_rulette_casino()
            bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}',  parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
            if result[0] == int(casino_mode):
                balance += (stavka * 35) + stavka
                bot.send_message(message.chat.id, f'Красава, ну тут я просто 👏👏👏\nДействие: +{stavka * 35}💵\nТвой баланс: {balance}💰')
            else:
                bot.send_message(message.chat.id, f'Анлак, тут выйграть - это реально везение\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            
            # Обновление данных balance для пользователя
            updataBalance(balance, message.from_user.id)
            
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
            bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
            bot.register_next_step_handler(message, roulette_cas)
    except:
        bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')

# Рулетка: Малые и Большие числа
def next_roulette_mb(message):
    global casino_mode
    global stavka
    global balance
    try:
        stavka = int(message.text)
        if check(stavka, balance) == False:
            bot.send_message(message.chat.id, 'Вы ввели некоректное значение.\nОтмена операции.')
        else:
            balance -= stavka
            result = game_rulette_casino()
            bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            if casino_mode == 'Малые числа':
                if result[0] < 19:
                    balance += stavka * 2
                    bot.send_message(message.chat.id, f'Повезло, поршивец!\nДействие: +{stavka}💵\nТвой баланс: {balance}💰')
                elif result[0] >= 19:
                    bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            elif casino_mode == 'Большие числа':
                if result[0] >= 19:
                    balance += stavka * 2
                    bot.send_message(message.chat.id, f'Повезло, поршивец!\nДействие: +{stavka}💵\nТвой баланс: {balance}💰')
                elif result[0] < 19:
                    bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            
            # Обновление данных balance для пользователя
            updataBalance(balance, message.from_user.id)
            
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
            bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
            bot.register_next_step_handler(message, roulette_cas)
    
    except:
        bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')

# Рулетка: Дюжины
def next_roulette_du(message):
    global casino_mode
    global stavka
    global balance
    try:
        stavka = int(message.text)
        if check(stavka, balance) == False:
            bot.send_message(message.chat.id, 'Вы ввели некоректное значение.\nОтмена операции.')
        else:
            balance -= stavka
            result = game_rulette_casino()
            bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            if casino_mode == 'Первая дюжина':
                if result[0] >= 1 and result[0] <= 12:
                    balance += (stavka * 2) + stavka
                    bot.send_message(message.chat.id, f'Еба, красава)\nДействие: +{stavka * 2}💵\nТвой баланс: {balance}💰')
                else:
                    bot.send_message(message.chat.id, f'Анлак\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            elif casino_mode == 'Вторая дюжина':
                if result[0] >= 13 and result[0] <= 24:
                    balance += (stavka * 2) + stavka
                    bot.send_message(message.chat.id, f'Еба, красава)\nДействие: +{stavka * 2}💵\nТвой баланс: {balance}💰')
                else:
                    bot.send_message(message.chat.id, f'Анлак\nДействие: -{stavka}💵\nТвой баланс: {balance}💰')
            elif casino_mode == 'Третья дюжина':
                if result[0] >= 25 and result[0] <= 36:
                    balance += (stavka * 2) + stavka
                    bot.send_message(message.chat.id, f'Еба, красава)\nДействие: +{stavka * 2}💵\nТвой баланс: {balance}')
                else:
                    bot.send_message(message.chat.id, f'Анлак\nДействие: -{stavka}💵\nТвой баланс: {balance}')
            
            # Обновление данных balance для пользователя
            updataBalance(balance, message.from_user.id)
            
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
            bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
            bot.register_next_step_handler(message, roulette_cas)
    except:
        bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')


# Обработка файла типа photo
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'И зачем ты мне это скинул?')


# Обработка /help
@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, 'Зачем тебе эта команда? Ты что тупой? Итак всё понятно')


# Обработка /info
@bot.message_handler(commands=['info'])
def info(message):
	bot.send_message(message.chat.id, message)
 

# Обработка всех текстовый сообщений
@bot.message_handler()
def messega_person(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'дарова' or message.text.lower() == 'ку' or message.text.lower() == 'салам':
        bot.send_message(message.chat.id, 'Хелоу')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == 'пока' or message.text.lower() == 'бб' or message.text.lower() == 'до свидания':
        bot.reply_to(message, f'Прощайте, {message.from_user.username}')


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    bot.polling(non_stop=True, skip_pending=True)