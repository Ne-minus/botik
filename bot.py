import osimport telebot

TOKEN = input("Введите токен:")  # '1663223369:AAH-yDDUkiJG33lUV5ZmHwsKg5uvHw3ISzM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text', '/reg'])
def start(message):
    if '/task' in message.text:
        bot.send_message(message.chat.id, "Задачу из какой домашки ты хочешь увидеть?")
        bot.register_next_step_handler(message, get_homework)


def get_homework(message):  # получаем номер домашки
    global homework
    homework = message.text
    bot.send_message(message.chat.id, 'Отправь мне номер задачи, и все будет сделано))')
    bot.register_next_step_handler(message, get_task)


def get_task(message):
    task = message.text
    filename = str(homework) + '_' + str(task) + '.txt'
    path = os.path.join('/home/hseguest/botik/tests', str(homework))
    path = os.path.join(path, str(filename))
    try:
        with open(path, encoding='utf-8') as f:
            bot.send_message(message.chat.id, text=f.read())
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Не могу найти задачу. Попробуем заново, задачу из какой домашки ты хочешь увидеть?')
        bot.register_next_step_handler(message, get_homework)


bot.polling()

