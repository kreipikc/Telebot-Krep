def setup_info_handlers(bot):
    @bot.message_handler(commands=['info'])
    def info(message):
        bot.send_message(message.chat.id, message)