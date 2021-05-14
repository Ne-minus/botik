import os
import telebot
import re
import urllib.request
import github
from github import Github

TOKEN = input("Введите токен:")  # '1663223369:AAH-yDDUkiJG33lUV5ZmHwsKg5uvHw3ISzM'
bot = telebot.TeleBot(TOKEN)
git_token = input('введите токен  гитхаб: ')
g = Github(git_token)
repo = g.get_repo('Ne-minus/botik')


@bot.message_handler(func=lambda message: message.forward_from is not None)  # getting a message forwarded from semicode
def update_hw(message):
    if 'Все задачи по' in message.text and message.forward_from.username == 'semicodebot':
        for entity in message.entities:  # getting a homework link from the message
            if entity.type == 'text_link':
                rep_link = entity.url
                break
        with urllib.request.urlopen(rep_link) as r:  # fishing for task links and homework number
            task_links = []
            pattern_task_link = r'(?<=<a href=")/[A-Za-z]+/[0-9a-z]+/raw/[0-9a-z]+/[0-9]+[.]{1}md(?=")'  # регуляр_очка
            pattern_hw = r'(?<=[HWhw-])+[0-9]+'
            check = 0
            for line in r:
                decoded = line.decode('utf-8')
                if ('<a href="/Pandaklez' in decoded or '<a href="/oserikov' in decoded or '<a href="/Sapunov' in decoded or '<a href="/lilaspourpre' in decoded) and '/raw/' in decoded:
                    for n in re.findall(pattern_task_link, decoded):
                        task_links.append('https://gist.githubusercontent.com' + n)
                elif '<title>' in decoded:
                    hw = re.findall(pattern_hw, decoded)[0]
                    path = os.path.join('tests', hw)
                    try:  # check if the homework already exists
                        contents = repo.get_contents(path)
                        bot.send_message(message.chat.id, 'данное дз уже в базе')
                        break
                    except github.GithubException:
                        check = 1
        if check == 1:  # upload tasks to github repo
            for i in range(len(task_links)):
                with urllib.request.urlopen(task_links[i]) as t:
                    task = t.read()
                path = os.path.join('tests', hw)
                filename = str(hw) + '_' + str(i + 1) + '.txt'
                path = os.path.join(path, str(filename))
                repo.create_file(path, 'upload', task)
                os.system('git pull')
            bot.send_message(message.chat.id, "Задачи обновлены")


@bot.message_handler(content_types=['text', '/reg'])
def asker(message):
    if 'задач' in message.text and 'Все задачи по' not in message.text:
        question = "Тебе нужна помощь с поиском задачи?"
        keyboard = telebot.types.InlineKeyboardMarkup()  # creating a  keyboard
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')  # button «Да»
        keyboard.add(key_yes)  # adding a button to the keyboard
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)
        # bot.register_next_step_handler(message, callback_worker)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Задачу из какой домашки ты хочешь увидеть?")
        bot.register_next_step_handler(call.message, get_homework)


def get_homework(message):  # getting the homework number
    global homework
    homework = message.text
    bot.send_message(message.chat.id, 'Отправь мне номер задачи, и все будет сделано))')
    bot.register_next_step_handler(message, get_task)


def get_task(message):  # getting the task number
    task = message.text
    filename = str(homework) + '_' + str(task) + '.txt'
    path = os.path.join('/home/hseguest/botik/tests', str(homework))
    path = os.path.join(path, str(filename))
    try:
        with open(path, encoding='utf-8') as f:
            bot.send_message(message.chat.id, text=f.read())
    except FileNotFoundError:
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_yes = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes)
        bot.send_message(message.chat.id, text='Не могу найти задачу. Попробуем заново?', reply_markup=keyboard)


def stopper(call):  # to stop working with the bot
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, "Задачу из какой домашки ты хочешь увидеть?")
        bot.register_next_step_handler(call.message, get_homework)
    elif call.data == 'no':
        return


bot.polling()

