import telebot
import constants
from datetime import datetime
import time
import sys
from library import library
import json
import editdistance


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
        range_bool = a in range(books.count() + 1)
    except:
        range_bool = False
    num_bool = (text.strip() == str(a))
    return num_bool & range_bool

def string_like_enough(search, source):  
    min_dist = max(len(search), len(source))
    min_dist = min(min_dist, editdistance.eval(search, source))

    i = 0

    while i + len(search) <= len(source):
        min_dist = min(min_dist, editdistance.eval(search, source[i:i+len(search)]))
        i += 1

    res = (min_dist <= min(len(search), len(source)) / 3)
    return res

def list_of_users():
    res = []

    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            if line.split(',')[1] != "0":
                res.append(line.split(',')[1])

    res = list(set(res))
    print(res)
    
    return res

def list_of_books(floor = "", searchString = ""):
    books = library(constants.filename_book_list)

    book_statuses = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            book_statuses[int(line.split(',')[0])] = [line.split(',')[1], str(int(line.split(',')[2]))]
            # book status : book_id, user_id, timestamp, floor
            if len(line.split(',')) >= 4:
                book_statuses[int(line.split(',')[0])].append(int(line.split(',')[3]))

    res = "Список книг:\n"
    
    for item in books.list():
        
        if int(book_statuses[item[0]][0]) != 0 and floor == "" and searchString == "":
            res += "/" + str(item[0]) + " (отдана) " + item[1]
            res += "\n"
        elif floor == "" and searchString == "":
            res += "/" + str(item[0]) + " " + item[1]
            if len(book_statuses[item[0]]) <= 2:
                res += " (24 этаж)"
            else:
                res += " (" + constants.bookshelfs[book_statuses[item[0]][2]] + ")"
            res += "\n"
        elif int(book_statuses[item[0]][0]) == 0 and floor != "" and searchString == "":
            if floor == constants.bookshelfs[book_statuses[item[0]][2]] and len(book_statuses[item[0]]) > 2:
                res += "/" + str(item[0]) + " " + item[1]
                res += "\n"
        elif searchString != "":
            if (string_like_enough(searchString.lower(), item[1].lower())):
                if int(book_statuses[item[0]][0]) != 0:
                    res += "/" + str(item[0]) + " (отдана) " + item[1]
                else:
                    res += "/" + str(item[0]) + " " + item[1]
                res += "\n"
    
    return res

def list_of_self_books(userId):
    books = library(constants.filename_book_list)

    book_statuses = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            book_statuses[int(line.split(',')[0])] = [line.split(',')[1], str(int(line.split(',')[2]))]
            # book status : book_id, user_id, timestamp, floor
            if len(line.split(',')) >= 4:
                book_statuses[int(line.split(',')[0])].append(int(line.split(',')[3]))

    res = "Список книг:"
    
    for item in books.list():
        if int(book_statuses[item[0]][0]) == userId:
            res += "\n/" + str(item[0]) + " " + item[1]

    return res
    

def get_book_from_shell(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            #print("OLOLO  put book on shelf 010 " + line.split(',')[0])
            #print(line)
            books[int(line.split(',')[0])] = [line.split(',')[1], str(int(line.split(',')[2]))]
            #print("OLOLO  put book on shelf 011 " + line.split(',')[0])
            if len(line.split(',')) > 3:
                books[int(line.split(',')[0])].append(int(line.split(',')[3]))
                #print("OLOLO  put book on shelf 012 " + line.split(',')[0])
            else:
                books[int(line.split(',')[0])].append(0)
                #print("OLOLO  put book on shelf 013 " + line.split(',')[0])
    #print(books)
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
    books[book_id][1] = str(round(time.time())) 
    books[book_id][2] = "0"
    with open(constants.filename_status,'w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1] + "," + str(books[item][2]) + "\n")
    logOperation("operation=Take book=" + str(book_id) + " success=True user=" + str(message.from_user.id))
    return True

## Здесь нужно научить бота работать с несколькими книгами!
def put_book_on_shell(book_id, message):
    books = dict()
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            books[int(line.split(',')[0])] = [line.split(',')[1], str(int(line.split(',')[2]))]
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

## Здесь бот начился работать с несколькими полками
def put_book_on_shelf(book_id, message):
    books = dict()
    #print("OLOLO  put book on shelf 01")
    with open(constants.filename_status,'r') as book_file:
        for line in book_file:
            #print("OLOLO  put book on shelf 010 " + line.split(',')[0])
            #print(line)
            books[int(line.split(',')[0])] = [line.split(',')[1], str(int(line.split(',')[2]))]
            #print("OLOLO  put book on shelf 011 " + line.split(',')[0])
            if len(line.split(',')) > 3:
                books[int(line.split(',')[0])].append(int(line.split(',')[3]))
                #print("OLOLO  put book on shelf 012 " + line.split(',')[0])
            else:
                books[int(line.split(',')[0])].append(0)
                #print("OLOLO  put book on shelf 013 " + line.split(',')[0])
    #print(books)
    #print("OLOLO  put book on shelf 02")

    if int(books[book_id][0]) == 0:
        logOperation("operation=Put book=" + str(book_id) + " success=False user=" + str(message.from_user.id))
        return False
    #print("OLOLO  put book on shelf 03")

    books[book_id][0] = "0"
    books[book_id][1] = str(round(time.time()))
    #print("OLOLO  put book on shelf 04")
    
    shelf_id = 0
    if message.text == "25 этаж":
        shelf_id = 1
    
    #print("OLOLO  put book on shelf 05")
    books[book_id][2] = shelf_id

    #print("OLOLO  put book on shelf 06")
    with open(constants.filename_status,'w') as book_file:
        for item in books:
            book_file.write(str(item) + "," + books[item][0] + "," + books[item][1] + "," + str(books[item][2]) + "\n")
    #print("OLOLO  put book on shelf 07")
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
                try:
                    answer = constants.message_collection.format(line.split(',')[0])
                    sent = bot.send_message(int(line.split(',')[1]), answer)
                    log(sent, answer)
                except:
                    log(message,"error writing to user" + str(line.split(',')[1]),)
    return True

@bot.message_handler(commands=['start'])
def handle_text(message):
    answer = constants.message_start
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')
    bot.send_message(message.chat.id, answer, reply_markup = user_markup)
    log(message, answer)

@bot.message_handler(commands=['help'])
def handle_text(message):
    answer = constants.message_help
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')
    bot.send_message(message.chat.id, answer, reply_markup = user_markup)
    log(message, answer)

@bot.message_handler(commands=['take'])
def handle_text(message):
    print("ROFL 01")
    maybe_number = message.text[5:].strip()
    print("ROFL 02")
    
    if maybe_number != "" and str(int(maybe_number)) == maybe_number and is_number(maybe_number):
        print("ROFL 02 01")
        if get_book_from_shell(int(maybe_number), message):
            print("ROFL 02 01 01")
            answer =  constants.message_you_got_book.format(maybe_number)#, 
                                                            #constants.lib[int(message.text.strip())][0])
        else:
            print("ROFL 02 01 02")
            answer = constants.message_already_taken
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
        user_markup.row('/list')
        user_markup.row('/return', '/take')
        user_markup.row('/help', '/suggest')
        
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer)
    else:
        print("ROFL 02 02")
        answer = constants.message_tell_book_number_get
        sent = bot.send_message(message.chat.id, answer)
        log(message, answer)
        bot.register_next_step_handler(sent, take_book)        
    

def take_book(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')

    if is_number(message.text):
        if get_book_from_shell(int(message.text), message):
            answer =  constants.message_you_got_book.format(message.text.strip())#, 
                                                            #constants.lib[int(message.text.strip())][0])
        else:
            answer = constants.message_already_taken
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer)
    else:
        answer = constants.message_bad_number
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer)

@bot.message_handler(commands=['return'])
def handle_text(message):
    answer = constants.message_tell_book_number_return
    sent = bot.send_message(message.chat.id, answer)
    log(message, answer)
    bot.register_next_step_handler(sent, return_book_choose_book)

def return_book_choose_book(message):
    global book_id
    if is_number(message.text):
        answer = constants.message_tell_shelf_number_return
        #print("OLOLO Return book set answer")
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
        user_markup.row('24 этаж','25 этаж')
        sent = bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        #print("OLOLO Return book sent message")
        log(message, answer)
        #print("OLOLO Return book log")
        book_id = int(message.text) 
        bot.register_next_step_handler(sent, return_book_choose_shelf)
    else:
        answer = constants.message_bad_number
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
        user_markup.row('/list')
        user_markup.row('/return', '/take')
        user_markup.row('/help', '/suggest')
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer)

def return_book_choose_shelf(message):
    global book_id
    if put_book_on_shelf(book_id, message):
        answer = constants.message_you_returned_book.format(str(book_id))#, 
                                                                #constants.lib[int(message.text.strip())][0])
        waiters_waiting = checkSubscriptionsForReturn(book_id, message)
        for waiter in waiters_waiting:
            bot.send_message(waiter, constants.message_subscribe_returned.format(str(book_id), message.text))
    else:
        answer = constants.message_already_returned    
    book_id = 0

    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')

    bot.send_message(message.chat.id, answer, reply_markup = user_markup)
    log(message, answer)

@bot.message_handler(commands=['list'])
def handle_text(message):
    answer = 'Какие книги хочешь посмотреть?'
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('24 этаж', '25 этаж')
    user_markup.row('Все', 'Поиск')
    user_markup.row('Книги у меня')
    
    sent = bot.send_message(message.chat.id, answer, reply_markup=user_markup)
    
    log(message, answer)

    bot.register_next_step_handler(sent, list_advanced)

def list_advanced(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')

    if message.text == 'Все':
        answer = list_of_books()
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer) 
    elif message.text == '24 этаж':
        answer = list_of_books(floor = "24 этаж")
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer) 
    elif message.text == '25 этаж':
        answer = list_of_books(floor = "25 этаж")
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer) 
    elif message.text == 'Поиск':
        answer = 'Введи поисковую строку'
        sent = bot.send_message(message.chat.id, answer)
        log(message, answer) 
        bot.register_next_step_handler(sent, list_search)
    elif message.text == 'Книги у меня':
        answer = list_of_self_books(userId = message.chat.id)
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer) 
    else:
        answer = 'Непонятно'
        bot.send_message(message.chat.id, answer, reply_markup = user_markup)
        log(message, answer)  


def list_search(message):
    answer = list_of_books(searchString = message.text)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')

    bot.send_message(message.chat.id, answer, reply_markup = user_markup)
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
    
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')
    
    bot.send_message(constants.manager, answer, reply_markup = user_markup)
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
    global book_id
    #print(current_book_num)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
    user_markup.row('/list')
    user_markup.row('/return', '/take')
    user_markup.row('/help', '/suggest')

    if current_book_num == 0:
        pass
    elif message.text == "Взять":
        if get_book_from_shell(current_book_num, message):
            answer =  constants.message_you_got_book.format(str(current_book_num))#, 
                                                            #constants.lib[current_book_num][0])
        else:
            answer = constants.message_already_taken
        bot.send_message(message.chat.id, answer, reply_markup=user_markup)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Положить":
        answer = constants.message_tell_shelf_number_return

        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)  
        user_markup.row('24 этаж','25 этаж')

        sent = bot.send_message(message.chat.id, answer, reply_markup = user_markup)

        book_id = current_book_num
        bot.register_next_step_handler(sent, return_book_choose_shelf)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Почитать описание":
        answer = book_info(current_book_num, message)
        bot.send_message(message.chat.id, answer, reply_markup=user_markup)
        current_book_num = 0
        log(message, answer)
    elif message.text == "Толкнуть читающего":
        result = ping_reader(current_book_num, message)
        if int(result) == 0:
            answer = constants.message_ping_requester_unsuccessfull    
        else:
            answer = constants.message_ping_requester_successfull
            ping_message = constants.message_ping_reader.format(str(current_book_num))
            try: 
                bot.send_message(result, ping_message)
            except:
                print("Reader is not in list")
                answer += "//problem with the reader"
        bot.send_message(message.chat.id, answer, reply_markup=user_markup)
        current_book_num = 0
        log(message, answer)    
    elif message.text == "Подписаться на возврат":
        subscribeForReturn(current_book_num, message)
        answer = constants.message_subscribe_successfull
        bot.send_message(message.chat.id, answer, reply_markup=user_markup)
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

@bot.message_handler(commands=['releasenotes'])
def handler_text(message):
    if message.chat.id == constants.manager:
        answer = constants.message_releasenotes_waiting
        sent = bot.send_message(message.chat.id, answer)
        log(message, answer)
        bot.register_next_step_handler(sent, send_releasenotes)
    else:
        answer = constants.message_releasenotes_forbidden
        bot.send_message(constants.manager, answer)
        log(message, answer)

def send_releasenotes(message):
    answer = constants.message_releasenotes_successfull
    users = list_of_users()
    for user in users:
        try:
            bot.send_message(user, message.text)
        except:
            bot.send_message(message.chat.id, constants.message_releasenotes_problem.format(str(user)))
    bot.send_message(message.chat.id, answer)
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



for i in range(3):
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except:
        bot.send_message(constants.manager, "Bot exception: " + str(i+1))
        bot.send_message(constants.manager, str(sys.exc_info()))
        print("Unexpected error:", sys.exc_info())
        with open("exceptions.log", "a") as errorlog:
            errorlog.write(str(datetime.now()) + " Unexpected error:" + str(sys.exc_info()) + "\n")

