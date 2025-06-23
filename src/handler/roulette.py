from telebot import types

from utils.check_format import check
from utils.roulette_casino import game_roulette_casino


casino_mode = None
bet = None
balance = 0

def setup_roulette_handlers(bot, database):
    @bot.message_handler(commands=['roulette'])
    def roulette_cas(message):
        database.add_user_db(message.from_user.id, message.from_user.username)

        if message.text == '/roulette' or message.text == 'Да, давай' or message.text.lower() == 'да' or message.text.lower() == '+' or message.text.lower() == 'yes':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row(types.KeyboardButton('👔 Мой профиль'))
            markup.row(types.KeyboardButton('Красное или Черное'), types.KeyboardButton('Нечетное или четное'))
            markup.row(types.KeyboardButton('Ставка на конкретное число'))
            markup.row(types.KeyboardButton('Ставка «Малые и большие номера»'), types.KeyboardButton('Дюжины'))
            bot.send_message(message.chat.id,
                             'Отлично! Значит хотим испытать удачу🍀?)\nНапоминаю правила игры, вы выбираете, как вы будете ставить, ставите и надеетесь на удачу!\nВсего 5 видов:\n1. На красное или черное\n2. Нечетное или четное\n3. Ставка на конкретное число\n4. Ставка «Малые и большие номера»\n5. Дюжины',
                             reply_markup=markup)
            bot.register_next_step_handler(message, next_roulette)
        else:
            bot.send_message(message.chat.id, 'Ну и не надо', reply_markup=types.ReplyKeyboardRemove())


    def next_roulette(message):
        if message.text == "👔 Мой профиль":
            profile(message)
        elif message.text == 'Красное или Черное' or message.text.strip() == '1' or message.text.strip() == '1.' or message.text.strip() == '1)':
            bot.send_message(message.chat.id,
                             'Хочу напомнить, в этом типе ставки ты можешь выбрать:\n🔴Красное🔴 или ⚫Черное⚫',
                             reply_markup=types.ReplyKeyboardRemove())
            markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup1.row(types.KeyboardButton('🔴Красное🔴'), types.KeyboardButton('⚫Черное⚫'))
            bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
            bot.register_next_step_handler(message, next_roulette_rate)
        elif message.text == 'Нечетное или четное' or message.text.strip() == '2' or message.text.strip() == '2.' or message.text.strip() == '2)':
            bot.send_message(message.chat.id, 'Хочу напомнить, в этом типе ставки ты можешь выбрать:\nЧетное или Нечетное',
                             reply_markup=types.ReplyKeyboardRemove())
            markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup1.row(types.KeyboardButton('Четное'), types.KeyboardButton('Нечетное'))
            bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
            bot.register_next_step_handler(message, next_roulette_rate)
        elif message.text == 'Ставка на конкретное число' or message.text.strip() == '3' or message.text.strip() == '3.' or message.text.strip() == '3)':
            bot.send_message(message.chat.id,
                             'Хочу напомнить, в этом типе ставки ты можешь выбрать число от 0 до 36\nДля ставки просто напишите число в чат',
                             reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, next_roulette_rate)
        elif message.text == 'Ставка «Малые и большие номера»' or message.text.strip() == '4' or message.text.strip() == '4.' or message.text.strip() == '4)':
            bot.send_message(message.chat.id,
                             'Хочу напомнить правила, в этом типе ставки ты можешь выбрать:\n1. Малые числа (от 1 до 18)\n2. Большие числа (от 19 до 36)',
                             reply_markup=types.ReplyKeyboardRemove())
            markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup1.row(types.KeyboardButton('Малые числа'), types.KeyboardButton('Большие числа'))
            bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
            bot.register_next_step_handler(message, next_roulette_rate)
        elif message.text == 'Дюжины' or message.text.strip() == '5' or message.text.strip() == '5.' or message.text.strip() == '5)':
            bot.send_message(message.chat.id,
                             'Хочу напомнить правила, в этом типе ставки ты можешь выбрать одну из 3 дюжин:\n1. Первая дюжина — числа от 1 до 12\n2. Вторая дюжина — числа от 13 до 24\n3. Третья дюжина — числа от 25 до 36',
                             reply_markup=types.ReplyKeyboardRemove())
            markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup1.row(types.KeyboardButton('Первая дюжина'))
            markup1.row(types.KeyboardButton('Вторая дюжина'))
            markup1.row(types.KeyboardButton('Третья дюжина'))
            bot.send_message(message.chat.id, 'Ну так что, на что ставим?', reply_markup=markup1)
            bot.register_next_step_handler(message, next_roulette_rate)


    # Вывод данных профиля игрока
    def profile(message):
        user = database.get_user_db(message.from_user.id)
        if user:
            bot.send_message(message.chat.id, f"Игрок: {user[0][3]}\nБаланс: {user[0][2]}💰")
            bot.send_message(message.chat.id,
                             "Не забудьте выбрать один из режимов игры:\n1. На красное или черное\n2. Нечетное или четное\n3. Ставка на конкретное число\n4. Ставка «Малые и большие номера»\n5. Дюжины")
            bot.register_next_step_handler(message, next_roulette)
        else:
            bot.send_message(message.chat.id, "Вы ещё не играли в игры!)")


    def next_roulette_rate(message):
        global casino_mode
        global balance
        casino_mode = message.text  # Сохранили на что ставим (красное, черное, число, первая дюжина и т.д.)
        user = database.get_user_db(message.from_user.id)
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
        elif casino_mode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                             '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
                             '33', '34', '35', '36']:
            bot.register_next_step_handler(message, next_roulette_number)


    # Рулетка: Красное-Черное
    def next_roulette_rb(message):
        global casino_mode
        global bet
        global balance
        try:
            bet = int(message.text)
            if not check(bet, balance):
                bot.send_message(message.chat.id, 'Вы ввели некорректное значение.\nОтмена операции.')
            else:
                balance -= bet
                result = game_roulette_casino()
                bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
                if casino_mode == "🔴Красное🔴" or casino_mode.lower() == "красное" or casino_mode.lower() == "к":
                    if result[1] == '🔴':
                        balance += bet * 2
                        bot.send_message(message.chat.id, f'Повезло, паршивец!\nДействие: +{bet}💵\nТвой баланс: {balance}💰')
                    elif result[1] == '⚫' or result[1] == '🟢':
                        bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                elif casino_mode == '⚫Черное⚫' or casino_mode.lower() == "черное" or casino_mode.lower() == "чёрное" or casino_mode.lower() == "ч":
                    if result[1] == '🔴':
                        bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                    elif result[1] == '⚫' or result[1] == '🟢':
                        balance += bet * 2
                        bot.send_message(message.chat.id, f'Повезло, паршивец!\nДействие: +{bet}💵\nТвой баланс: {balance}💰')

                # Обновление данных balance для пользователя
                database.update_balance(balance, message.from_user.id)

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
                bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
                bot.register_next_step_handler(message, roulette_cas)
        except:
            bot.send_message(message.chat.id, 'Вы ввели некорректное значение.\nОтмена операции.')


    # Рулетка: Четные-Нечетные
    def next_roulette_dch(message):
        global casino_mode
        global bet
        global balance
        try:
            bet = int(message.text)
            if not check(bet, balance):
                bot.send_message(message.chat.id, 'Вы ввели некорректное значение.\nОтмена операции.')
            else:
                balance -= bet
                result = game_roulette_casino()
                bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
                if casino_mode == 'Четное':
                    if result[0] % 2 == 0:
                        balance += bet * 2
                        bot.send_message(message.chat.id, f'Повезло, паршивец!\nДействие: +{bet}💵\nТвой баланс: {balance}💰')
                    elif result[0] % 2 != 0 or result[0] == 0:
                        bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                elif casino_mode == 'Нечетное':
                    if result[0] % 2 == 0 or result[0] == 0:
                        bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                    elif result[0] % 2 != 0:
                        balance += bet * 2
                        bot.send_message(message.chat.id, f'Повезло, паршивец!\nДействие: +{bet}💵\nТвой баланс: {balance}💰')

                # Обновление данных balance для пользователя
                database.update_balance(balance, message.from_user.id)

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
                bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
                bot.register_next_step_handler(message, roulette_cas)
        except:
            bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')


    # Рулетка: Конкретное число
    def next_roulette_number(message):
        global casino_mode
        global bet
        global balance
        try:
            bet = int(message.text)
            if not check(bet, balance):
                bot.send_message(message.chat.id, 'Вы ввели некорректное значение.\nОтмена операции.')
            else:
                balance -= bet
                result = game_roulette_casino()
                bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}', parse_mode='html',
                                 reply_markup=types.ReplyKeyboardRemove())
                if result[0] == int(casino_mode):
                    balance += (bet * 35) + bet
                    bot.send_message(message.chat.id,
                                     f'Красава, ну тут я просто 👏👏👏\nДействие: +{bet * 35}💵\nТвой баланс: {balance}💰')
                else:
                    bot.send_message(message.chat.id,
                                     f'Анлак, тут выйграть - это реально везение\nДействие: -{bet}💵\nТвой баланс: {balance}💰')

                # Обновление данных balance для пользователя
                database.update_balance(balance, message.from_user.id)

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
                bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
                bot.register_next_step_handler(message, roulette_cas)
        except:
            bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')


    # Рулетка: Малые и Большие числа
    def next_roulette_mb(message):
        global casino_mode
        global bet
        global balance
        try:
            bet = int(message.text)
            if not check(bet, balance):
                bot.send_message(message.chat.id, 'Вы ввели некорректное значение.\nОтмена операции.')
            else:
                balance -= bet
                result = game_roulette_casino()
                bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
                if casino_mode == 'Малые числа':
                    if result[0] < 19:
                        balance += bet * 2
                        bot.send_message(message.chat.id, f'Повезло, паршивец!\nДействие: +{bet}💵\nТвой баланс: {balance}💰')
                    elif result[0] >= 19:
                        bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                elif casino_mode == 'Большие числа':
                    if result[0] >= 19:
                        balance += bet * 2
                        bot.send_message(message.chat.id, f'Повезло, паршивец!\nДействие: +{bet}💵\nТвой баланс: {balance}💰')
                    elif result[0] < 19:
                        bot.send_message(message.chat.id, f'Какая досада)\nДействие: -{bet}💵\nТвой баланс: {balance}💰')

                # Обновление данных balance для пользователя
                database.update_balance(balance, message.from_user.id)

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
                bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
                bot.register_next_step_handler(message, roulette_cas)

        except:
            bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')


    # Рулетка: Дюжины
    def next_roulette_du(message):
        global casino_mode
        global bet
        global balance
        try:
            bet = int(message.text)
            if not check(bet, balance):
                bot.send_message(message.chat.id, 'Вы ввели некорректное значение.\nОтмена операции.')
            else:
                balance -= bet
                result = game_roulette_casino()
                bot.send_message(message.chat.id, f'Выпало:\n{result[1]} <b>{result[0]}</b> {result[1]}',
                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
                if casino_mode == 'Первая дюжина':
                    if 1 <= result[0] <= 12:
                        balance += (bet * 2) + bet
                        bot.send_message(message.chat.id, f'Еба, красава)\nДействие: +{bet * 2}💵\nТвой баланс: {balance}💰')
                    else:
                        bot.send_message(message.chat.id, f'Анлак\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                elif casino_mode == 'Вторая дюжина':
                    if 13 <= result[0] <= 24:
                        balance += (bet * 2) + bet
                        bot.send_message(message.chat.id, f'Еба, красава)\nДействие: +{bet * 2}💵\nТвой баланс: {balance}💰')
                    else:
                        bot.send_message(message.chat.id, f'Анлак\nДействие: -{bet}💵\nТвой баланс: {balance}💰')
                elif casino_mode == 'Третья дюжина':
                    if 25 <= result[0] <= 36:
                        balance += (bet * 2) + bet
                        bot.send_message(message.chat.id, f'Еба, красава)\nДействие: +{bet * 2}💵\nТвой баланс: {balance}')
                    else:
                        bot.send_message(message.chat.id, f'Анлак\nДействие: -{bet}💵\nТвой баланс: {balance}')

                # Обновление данных balance для пользователя
                database.update_balance(balance, message.from_user.id)

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row(types.KeyboardButton('Да, давай'), types.KeyboardButton('Я пас'))
                bot.send_message(message.chat.id, 'Ещё будем играть?', reply_markup=markup)
                bot.register_next_step_handler(message, roulette_cas)
        except:
            bot.send_message(message.chat.id, 'Ставка записана некорректно.\nОтмена операции.')