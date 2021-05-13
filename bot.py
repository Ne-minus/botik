import os
import telebot
from telebot import types
import re
import urllib.request
import github
from github import Github

TOKEN = input("Введите токен:")  # '1663223369:AAH-yDDUkiJG33lUV5ZmHwsKg5uvHw3ISzM'
bot = telebot.TeleBot(TOKEN)
username = input('введите логин гитхаб: ')
password = input('введите пароль гитхаб: ')
g = Github(username, password)
repo = g.get_repo('Ne-minus/botik')



@bot.message_handler(func=lambda message: message.forward_from is not None)
def update_hw(message):
    if 'Все задачи по' in message.text and message.forward_from.username == 'semicodebot':
        for entity in message.entities:
            if entity.type == 'text_link':
                rep_link = entity.url
                break
        with urllib.request.urlopen(rep_link) as r:
            task_links = []
            pattern_task_link = r'(?<=<a href=")/Pandaklez/[0-9a-z]+/raw/[0-9a-z]+/[0-9]+[.]{1}md(?=")'  # регуляр_очка
            pattern_hw = r'(?<=[HWhw-])+[0-9]+'
            check = 0
            for line in r:
                decoded = line.decode('utf-8')
                if '<a href="/Pandaklez' in decoded and '/raw/' in decoded:
                    for n in re.findall(pattern_task_link, decoded):
                        task_links.append('https://gist.githubusercontent.com'+n)
                elif '<title>' in decoded:
                    hw = re.findall(pattern_hw, decoded)[0]
                    path = os.path.join('/tests', hw)
                    try:
                        contents = repo.get_contents(path)
                        for c in contents:
                            bot.send_message(message.chat.id, c)
                        bot.send_message(message.chat.id, 'данное дз уже в базе')
                        break
                    except github.GithubException:
                        check = 1
        if check == 1:
            for i in range(len(task_links)):
                with urllib.request.urlopen(task_links[i]) as t:
                    task = t.read()
                path = os.path.join('/tests', hw)
                filename = str(hw) + '_' + str(i+1) + '.txt'
                path = os.path.join(path, str(filename))
                repo.create_file(path, 'upload', task)
            bot.send_message(message.chat.id, "Задачи обновлены")


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
