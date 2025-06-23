def setup_help_handlers(bot):
    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot.send_message(message.chat.id, 'Зачем тебе эта команда? Ты что тупой? Итак всё понятно')