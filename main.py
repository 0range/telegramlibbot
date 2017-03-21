import telebot
import constants
from datetime import datetime
import time
import sys
from library import library
import json


print(constants.message_start_bot)

bot = telebot.TeleBot(constants.token)

current_book_num = 0

def logprint(text):
    filename = constants.filename_log_name + "_" + str(datetime.now()).split(' ')[0] + constants.filename_log_extension
    with open(filename,'a') as logfile:
        logfile.write(text)
    print(text)

def logOperation(string):
    with open(constants.filename_log_operation, 'a') as logfile:
        logfile.write(str(datetime.now()) + " " + string + " \n")

def log(message, answer):
    logprint(str(datetime.now()) + " ")
    logprint(constants.log_text.format(message.from_user.first_name,
                                       message.from_user.last_name,
                                       str(message.from_user.id),
                                       message.text,
                                       answer))

def subscribeForReturn(book_id, message):
    subscriptions = dict()
    
    try:
        with open(constants.filename_return_subscriptions) as data_file:
            subscriptions = json.load(data_file)
    except:
        pass

    if str(book_id) in subscriptions:
        if message.from_user.id in subscriptions[str(book_id)]:
            pass
        else:
            subscriptions[str(book_id)].append(message.from_user.id)
    else:    
        subscriptions[str(book_id)] = [message.from_user.id]

    with open(constants.filename_return_subscriptions, 'w') as outfile:
        json.dump(subscriptions, outfile)

    return True

def checkSubscriptionsForReturn(book_id, message):
    subscriptions = dict()
    result = []

    try:
        with open(constants.filename_return_subscriptions) as data_file:
            subscriptions = json.load(data_file)
    except:
        pass

    if str(book_id) in subscriptions:
        result = subscriptions[str(book_id)]
        subscriptions[str(book_id)] = []

    with open(constants.filename_return_subscriptions, 'w') as outfile:
        json.dump(subscriptions, outfile)
    
    return result

def is_number(text):
    books = library(constants.filename_book_list)
    a = 0
    range_bool = True
    try:
        a = int(text)
        range_bool = a in range(books.count())
    except:
        range_bool = False
    num_bool = (text.strip() == str(a))
    return num_bool & range_bool

def list_of_books():
    books = library(constants.filename_book_list)

    book_statuses = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            book_statuses[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]

    res = "Список книг:\n"
    
    for item in books.list():
        
        if int(book_statuses[item[0]][0]) != 0:
            res += "/" + str(item[0]) + " (отдана) " + item[1]
        else:
            res += "/" + str(item[0]) + " " + item[1]
        res += "\n"
    
    return res

def get_book_from_shell(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    #print(books)

    if int(books[book_id][0]) != 0:
        logOperation("operation=Take book=" + str(book_id) + " success=False user=" + str(message.from_user.id))
        return False
    
    #print("Getting book from shelf")
    taken_books_counter = 0
    for book in books:
        print(books[book])
        if int(books[book][0]) == message.from_user.id:
            taken_books_counter += 1
    if taken_books_counter >= 2:
        logOperation("operation=Take book=" + str(book_id) + " success=False user=" + str(message.from_user.id)) 
        return False
    #print(taken_books_counter)
    
    books[book_id][0] = str(message.from_user.id)
    books[book_id][1] = str(round(time.time())) + "\n"
    with open(constants.filename_status,'w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1])
    logOperation("operation=Take book=" + str(book_id) + " success=True user=" + str(message.from_user.id))
    return True

def put_book_on_shell(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    #print(books)

    if int(books[book_id][0]) == 0:
        logOperation("operation=Put book=" + str(book_id) + " success=False user=" + str(message.from_user.id))
        return False

    books[book_id][0] = "0"
    books[book_id][1] = str(round(time.time())) + "\n"
    with open(constants.filename_status,'w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1])
    logOperation("operation=Put book=" + str(book_id) + " success=True user=" + str(message.from_user.id))
    return True

def ping_reader(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    logOperation("operation=Ping book=" + str(book_id) + " success=True user=" + str(message.from_user.id))
    return books[book_id][0]

def book_info(book_id, message):
    books = library(constants.filename_book_list)
    logOperation("operation=Info book=" + str(book_id) + " success=True user=" + str(message.from_user.id))
    return(books.bookInfo(book_id))#constants.lib[book_id][0] + "\n " + constants.lib[book_id][1])

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
            answer =  constants.message_you_got_book.format(message.text.strip())#, 
                                                            #constants.lib[int(message.text.strip())][0])
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
            answer = constants.message_you_returned_book.format(message.text.strip())#, 
                                                                #constants.lib[int(message.text.strip())][0])
            waiters_waiting = checkSubscriptionsForReturn(int(message.text), message)
            for waiter in waiters_waiting:
                bot.send_message(waiter, constants.message_subscribe_returned.format(message.text))
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

@bot.message_handler(commands=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25',
'26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50',
'51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75',
'76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99'])
def handle_text(message):
    global current_book_num
    answer = constants.message_what_to_do
    current_book_num = int(message.text[1:].strip())
    #print(current_book_num)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Почитать описание')

    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], line.split(',')[2]]
    #print(books)

    if int(books[current_book_num][0]) != 0:
        user_markup.row('Подписаться на возврат')
        user_markup.row('Толкнуть читающего')
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
            answer =  constants.message_you_got_book.format(str(current_book_num))#, 
                                                            #constants.lib[current_book_num][0])
        else:
            answer = constants.message_already_taken
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Положить":
        if put_book_on_shell(current_book_num, message):
            answer = constants.message_you_returned_book.format(str(current_book_num))#, 
                                                                #constants.lib[current_book_num][0])
            waiters_waiting = checkSubscriptionsForReturn(current_book_num, message)
            for waiter in waiters_waiting:
                bot.send_message(waiter, constants.message_subscribe_returned.format(str(current_book_num)))
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
    elif message.text == "Толкнуть читающего":
        result = ping_reader(current_book_num, message)
        if int(result) == 0:
            answer = constants.message_ping_requester_unsuccessfull    
        else:
            answer = constants.message_ping_requester_successfull
            ping_message = constants.message_ping_reader.format(str(current_book_num))
            bot.send_message(result, ping_message)
        bot.send_message(message.chat.id, answer)
        current_book_num = 0
        log(message, answer)    
    elif message.text == "Подписаться на возврат":
        subscribeForReturn(current_book_num, message)
        answer = constants.message_subscribe_successfull
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

@bot.message_handler(commands=['add'])
def handler_text(message):
    if message.from_user.id == constants.manager:
        answer = constants.message_addbook_name
    else:
        answer = constants.message_addbook_mistaken
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, add_new_book)

def add_new_book(message):
    global new_book 
    new_book = ["","",""]
    new_book[0] = message.text
    answer = constants.message_addbook_description
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, add_new_book_description)

def add_new_book_description(message):
    global new_book
    new_book[1] = message.text
    books = library(constants.filename_book_list)
    books.add(new_book)
    answer = constants.message_addbook_success
    bot.send_message(message.chat.id, answer)
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



for i in range(1):
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except:
        bot.send_message(constants.manager, "Bot exception: " + str(i+1))
        bot.send_message(constants.manager, str(sys.exc_info()))
        print("Unexpected error:", sys.exc_info())
        with open("exceptions.log", "a") as errorlog:
            errorlog.write(str(datetime.now()) + " Unexpected error:" + str(sys.exc_info()) + "\n")

