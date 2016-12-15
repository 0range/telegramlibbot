import telebot
import tokens
from datetime import datetime
import time
import json

lib = dict({1: "Алистер Коберн. Современные методы описания функциональных требований к системам",
2: "Глеб Архангельский. Тайм-драйв",
3: "Михаил Литвак. Командовать или подчиняться",
4: "Джефф Сазерленд. SCRUM",
5: "Девид Аллен. Как привести дела в порядок",
6: "Эрик Рис. Бизнес с нуля",
7: "Ицхак Адизес. Идеальный руководитель",
8: "Ицхак Адизес. Развитие лидеров",
9: "Олег Тиньков. Я такой как все",
10: "Олег Тиньков. Я такой как все",
11: "Ф.Брукс. Мифический человеко-месяц",
12: "Г.Кеннеди. Договориться можно обо всем"})

bot = telebot.TeleBot(tokens.token)

current_book_num = 0

def log(message, answer):
    print(datetime.now())
    print("Сообщение \nОт {0} {1}. [id = {2}]. Текст: {3}".format(message.from_user.first_name,
                                                                  message.from_user.last_name,
                                                                  str(message.from_user.id),
                                                                  message.text))
    print("Ответ Бота:\n", answer)
    print("---")

def is_number(text):
    a = 0
    range_bool = True
    try:
        a = int(text)
        range_bool = a in lib
    except:
        range_bool = False
    num_bool = (text.strip() == str(a))
    return num_bool & range_bool

def list_of_books():
    res = "Список книг:\n"
    for item in lib:
        res += "/" + str(item) + " : "
        res += lib[item]
        res += "\n"
    return res

def get_book_from_shell(book_id, message):
    books = dict()
    with open('books_status.data','r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    print(books)
    if int(books[book_id][0]) != 0:
        return False
    books[book_id][0] = str(message.from_user.id)
    books[book_id][1] = str(round(time.time())) + "\n"
    with open('books_status.data','w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1])
    return True

def put_book_on_shell(book_id, message):
    books = dict()
    with open('books_status.data','r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    print(books)
    if int(books[book_id][0]) == 0:
        return False
    books[book_id][0] = "0"
    books[book_id][1] = str(round(time.time())) + "\n"
    with open('books_status.data','w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1])
    return True

#bot.send_message(81593382, "Tst")

#upd = bot.get_updates()
#print(upd)
#last_update = upd[-1]
#last_msg_from_user = last_update.message
#print(last_msg_from_user)


@bot.message_handler(commands=['start'])
def handle_text(message):
    answer = """Привет! Я бот-библиотекарь в SME.
Скажи мне, какую книжку ты хочешь взять, и я тебя запишу ;)

Пообщаться со мной можно так:
/take - Взять книгу с полки
/return - Вернуть книгу на полку
/list - Посмотреть, что лежит на полке

и, конечно
/help - Список команд"""
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['help'])
def handle_text(message):
    answer = """Напоминаю:
/take - Взять книгу с полки
/return - Вернуть книгу на полку
/list - Посмотреть, что лежит на полке

/help - Список команд"""
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['take'])
def handle_text(message):
    answer = "Скажи номер книги, которую хочешь взять"
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, take_book)

def take_book(message):
    if is_number(message.text):
        if get_book_from_shell(int(message.text), message):
            answer =  "Отлично, книга номер {0} теперь у тебя".format(message.text.strip())
        else:
            answer = "Кажется, эту книгу уже забрали"
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        answer = "Извини, непонятный номер книги :("
        bot.send_message(message.chat.id, answer)
        log(message, answer)

@bot.message_handler(commands=['return'])
def handle_text(message):
    answer = "Скажи номер книги, которую возвращаешь"
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, return_book)

def return_book(message):
    if is_number(message.text):
        if put_book_on_shell(int(message.text), message):
            answer = "Отлично, книга номер {0} вернулась на полку. Спасибо!".format(message.text.strip())
        else:
            answer = "Кажется, эта книга уже на полке"
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        answer = "Извини, непонятный номер книги :("
        bot.send_message(message.chat.id, answer)
        log(message, answer)

@bot.message_handler(commands=['list'])
def handle_text(message):
    answer = list_of_books()
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['1','2','3','4','5','6','7','8','9','10','11','12'])
def handle_text(message):
    global current_book_num
    answer = "Ты выбрал книгу - что с ней делать?"
    current_book_num = int(message.text[1:].strip())
    #print(current_book_num)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Взять', 'Положить')
    sent = bot.send_message(message.chat.id, answer, reply_markup=user_markup)
    log(message, answer)
    bot.register_next_step_handler(sent, manage_book)

def manage_book(message):
    global  current_book_num
    #print(current_book_num)
    if current_book_num == 0:
        pass
    elif message.text == "Взять":
        if get_book_from_shell(current_book_num, message):
            answer =  "Отлично, книга номер {0} теперь у тебя".format(str(current_book_num))
        else:
            answer = "Кажется, эту книгу уже забрали"
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Положить":
        if put_book_on_shell(current_book_num, message):
            answer = "Отлично, книга номер {0} вернулась на полку. Спасибо!".format(str(current_book_num))
        else:
            answer = "Кажется, эта книга уже на полке"
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)


#@bot.message_handler(content_types=['text'])
#def handle_text(message):
#    if message.text == 'hello':
#        answer = "Hello, human"
#    elif message.text == 'Bye':
#        answer =  "Good bye, human"
#    else:
#        answer = "Прости, я тебя не понимаю. Может, пришло время начать все сначала?"
#    log(message, answer)


bot.polling(none_stop=True, interval=0)
