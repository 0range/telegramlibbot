import telebot
import constants
from datetime import datetime
import time
import sys

print(constants.message_start_bot)

bot = telebot.TeleBot(constants.token)

current_book_num = 0

def logprint(text):
    filename = constants.filename_log_name + "_" + str(datetime.now()).split(' ')[0] + constants.filename_log_extension
    with open(filename,'a') as logfile:
        logfile.write(text)
    print(text)

def log(message, answer):
    logprint(str(datetime.now()) + " ")
    logprint(constants.log_text.format(message.from_user.first_name,
                                       message.from_user.last_name,
                                       str(message.from_user.id),
                                       message.text,
                                       answer))

def is_number(text):
    a = 0
    range_bool = True
    try:
        a = int(text)
        range_bool = a in constants.lib
    except:
        range_bool = False
    num_bool = (text.strip() == str(a))
    return num_bool & range_bool

def list_of_books():
    books = dict()
    res = "Список книг:\n"
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    for item in constants.lib:
        res += "/" + str(item) + " : "
        if int(books[item][0]) != 0:
            res += " (отдана) "
        res += constants.lib[item][0]
        res += "\n"
    return res

def get_book_from_shell(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    print(books)
    if int(books[book_id][0]) != 0:
        return False
    books[book_id][0] = str(message.from_user.id)
    books[book_id][1] = str(round(time.time())) + "\n"
    with open(constants.filename_status,'w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1])
    return True

def put_book_on_shell(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    print(books)
    if int(books[book_id][0]) == 0:
        return False
    books[book_id][0] = "0"
    books[book_id][1] = str(round(time.time())) + "\n"
    with open(constants.filename_status,'w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1])
    return True

def book_info(book_id, message):
    return(constants.lib[book_id][0] + "\n " + constants.lib[book_id][1])

def collect(message):
    if message.from_user.id != constants.manager:
        return false
    #collect
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            if int(line.split(',')[1]) != 0 and round(time.time()) - constants.collection_time > int(line.split(',')[2]):
                #print("Starting collection...   " + line)
                answer = constants.message_collection.format(line.split(',')[0])
                sent = bot.send_message(int(line.split(',')[1]), answer)
                log(sent, answer)
    return True

@bot.message_handler(commands=['start'])
def handle_text(message):
    answer = constants.message_start
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['help'])
def handle_text(message):
    answer = constants.message_help
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['take'])
def handle_text(message):
    answer = constants.message_tell_book_number_get
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, take_book)

def take_book(message):
    if is_number(message.text):
        if get_book_from_shell(int(message.text), message):
            answer =  constants.message_you_got_book.format(message.text.strip(), 
                                                            constants.lib[int(message.text.strip())][0])
        else:
            answer = constants.message_already_taken
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        answer = constants.message_bad_number
        bot.send_message(message.chat.id, answer)
        log(message, answer)

@bot.message_handler(commands=['return'])
def handle_text(message):
    answer = constants.message_tell_book_number_return
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, return_book)

def return_book(message):
    if is_number(message.text):
        if put_book_on_shell(int(message.text), message):
            answer = constants.message_you_returned_book.format(message.text.strip(), 
                                                                constants.lib[int(message.text.strip())][0])
        else:
            answer = constants.message_already_returned
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        answer = constants.message_bad_number
        bot.send_message(message.chat.id, answer)
        log(message, answer)

@bot.message_handler(commands=['list'])
def handle_text(message):
    answer = list_of_books()
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['suggest'])
def handle_text(message):
    answer = constants.message_suggest_cool
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, get_book_suggestion)

def get_book_suggestion(message):
    answer = constants.message_thanks_for_suggest
    bot.send_message(message.chat.id, answer)
    log(message, answer)
    answer = constants.message_suggest_prefix + message.text
    bot.send_message(constants.manager, answer)
    log(message, answer)

@bot.message_handler(commands=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])
def handle_text(message):
    global current_book_num
    answer = constants.message_what_to_do
    current_book_num = int(message.text[1:].strip())
    #print(current_book_num)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Взять', 'Положить')
    user_markup.row('Почитать описание')
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
            answer =  constants.message_you_got_book.format(str(current_book_num), 
                                                            constants.lib[current_book_num][0])
        else:
            answer = constants.message_already_taken
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Положить":
        if put_book_on_shell(current_book_num, message):
            answer = constants.message_you_returned_book.format(str(current_book_num), 
                                                                constants.lib[current_book_num][0])
        else: 
            answer = constants.message_already_returned
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Почитать описание":
        answer = book_info(current_book_num, message)
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)

@bot.message_handler(commands=['collect'])
def handler_text(message):
    if collect(message):
        answer = constants.message_collection_successfull
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        answer = constants.message_collection_forbidden
        bot.send_message(constants.manager, answer)
        log(message, answer)  

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == constants.message_stupid_bot:
        answer = constants.message_stupid_bot_reply
        bot.send_message(message.chat.id, answer)
        log(message, answer)   
    elif message.text.strip() in [':)',';)']:
        answer = ';)'
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif message.chat.id == constants.manager:
        answer = constants.message_healthcheck
        bot.send_message(message.chat.id, answer)
        log(message, answer) 
    else:
        answer = "!no answer"
        log(message, answer)



for i in range(100):
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except:
        print("Unexpected error:", sys.exc_info())
        with open("exceptions.log", "a") as errorlog:
            errorlog.write(str(datetime.now()) + " Unexpected error:" + str(sys.exc_info()) + "\n")
