def setup_other_handlers(bot):
    # Обработка файла типа photo
    @bot.message_handler(content_types=['photo'])
    def get_photo(message):
        bot.reply_to(message, 'И зачем ты мне это скинул?')

    # Обработка всех текстовый сообщений
    @bot.message_handler()
    def message_person(message):
        if message.text.lower() == 'привет' or message.text.lower() == 'дарова' or message.text.lower() == 'ку' or message.text.lower() == 'салам':
            bot.send_message(message.chat.id, 'Хелоу')
        elif message.text.lower() == 'id':
            bot.reply_to(message, f'ID: {message.from_user.id}')
        elif message.text.lower() == 'пока' or message.text.lower() == 'бб' or message.text.lower() == 'до свидания':
            bot.reply_to(message, f'Прощайте, {message.from_user.username}')