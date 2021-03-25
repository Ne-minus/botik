# from telebot import types
import os
import telebot

TOKEN = input("введите тоен:")  # '1663223369:AAH-yDDUkiJG33lUV5ZmHwsKg5uvHw3ISzM'
bot = telebot.TeleBot(TOKEN)
name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text', '/reg'])
def start(message):
    # if message.text == '/reg':
    if 'задач' in message.text:
        bot.send_message(message.chat.id, "Задачу из какой домашки ты хочешь увидеть?")
        bot.register_next_step_handler(message, homeworks)
    # else:
    # bot.send_message(message.from_user.id, 'Напиши /reg')


def homeworks(message):  # получаем номер домашки
    global homework
    homework = message.text
    bot.send_message(message.chat.id, 'Отправь мне номер задачи, и все будет сделано))')
    bot.register_next_step_handler(message, task)


def task(message):
    # global task
    global filename, text1, task, path
    task = message.text
    # bot.send_message(message.from_user.id,'Сколько тебе лет?')
    # bot.register_next_step_handler(message, get_age)
    filename = homework + '_' + task + '.txt'
    path = os.path.join('botik/tests', homework)
    path = os.path.join(path, filename)
    with open(path, encoding='utf-8') as f:
        bot.send_message(message.chat.id, text=f.read())


'''
def get_age(message):
    global age
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')#кнопка «Да»
        keyboard.add(key_yes) #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    age = 0
#@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.from_user.id, text='Я молодец!)')
    elif call.data == "no":
        bot.send_message(call.from_user.id, text='Жаль. Но я только учусь!')
#bot.polling('none_stop=True, interval=0')
'''
bot.polling()
