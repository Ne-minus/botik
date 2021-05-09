import os
import telebot
from telebot import types
import re
import urllib.request

TOKEN = input("Введите токен:")  # '1663223369:AAH-yDDUkiJG33lUV5ZmHwsKg5uvHw3ISzM'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: message.forward_from is not None)
def update_hw(message):
    if 'Все задачи по' in message.text and message.forward_from.username == 'semicodebot':
        for entity in message.entities:
            if entity.type == 'text_link':
                rep_link = entity.url
                break
        with urllib.request.urlopen(rep_link) as r:
            task_links = []
            pattern_task_link = r'(?<=<a href=" )/Pandaklez/[0-9a-z]+/raw/[0-9a-z]+/[0-9]+[.]{1}md(?=" role="button")'  # регуляяяяяр_очка
            pattern_hw = r'(?<=<title>)[HWhw-]+[0-9]+'
            for line in r:
                decoded = line.decode('utf-8')
                if '<a href="/Pandaklez' in decoded and '/raw/' in decoded:
                    task_links.extend(re.findall(pattern_task_link, decoded))
                elif '<title>' in decoded:
                    hw = re.findall(pattern_hw, decoded)[0]
        bot.send_message(message.chat.id, task_links[1])


@bot.message_handler(content_types=['text', '/reg'])
def asker(message):
    if 'задач' in message.text and 'Все задачи по' not in message.text:
        question = "Вам нужна помощь с поиском задачи?"
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
        keyboard.add(key_yes) #добавляем кнопку в клавиатуру
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)
        #bot.register_next_step_handler(message, callback_worker)


@bot.callback_query_handler(func=lambda call: True)        
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Задачу из какой домашки ты хочешь увидеть?")
        bot.register_next_step_handler(call.message, get_homework)
    
            
#def start(message):
 #   print(1337)
 #   bot.send_message(message.chat.id, "Задачу из какой домашки ты хочешь увидеть?")
#  bot.register_next_step_handler(call.message, get_homework)


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
