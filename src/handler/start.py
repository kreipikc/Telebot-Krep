from telebot import types


def setup_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
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
            bot.send_message(callback.message.chat.id, 'Ну лан, давай поболтаем, что как ты?')