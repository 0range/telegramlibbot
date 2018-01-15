
token = "370650649:AAGnrKtBZLViwxm0faRBFfdFVXECTiAkrWQ"

manager = 81593382
collection_time = 1209600

filename_status = "books_status.data"
filename_book_list = "book_list.json"
filename_log_name = "log"
filename_log_extension = ".log"
filename_log_operation = "operations.log"
filename_return_subscriptions = "return_subscriptions.json"

log_text = "name=\"{0}\" surname=\"{1}\" id={2} text=\"{3}\" answer=\"{4}\" \n"

message_start_bot = "Bot initialised"
message_start = """Привет! Я бот-библиотекарь в SME.
Скажи мне, какую книжку ты хочешь взять, и я тебя запишу ;)

Пообщаться со мной можно так:
/list - Посмотреть, что лежит на полке
/take - Взять книгу с полки
/return - Вернуть книгу на полку
/n, где n это номер книги - Действия с этой книгой

и, конечно
/help - Список команд"""
message_help =  """Напоминаю:
/list - Посмотреть, что лежит на полке
/take - Взять книгу с полки
/return - Вернуть книгу на полку
/n, где n это номер книги - Действия с этой книгой. Это самая интересная опция, вызови список и просто ткни на номер книги в начале строки - увидишь, что можно сделать

/help - Список команд"""
message_tell_book_number_get = "Скажи номер книги, которую хочешь взять"
message_tell_book_number_return = "Скажи номер книги, которую возвращаешь"
message_tell_shelf_number_return = "Скажи полку, на которую поставить книгу"
message_already_taken = "Кажется, эту книгу уже забрали. Или у тебя слишком много книг"
message_you_got_book = "Отлично, книга номер {0} теперь у тебя"
message_already_returned = "Кажется, эта книга уже на полке"
message_you_returned_book = "Отлично, книга номер {0} вернулась на полку. Спасибо!"
message_bad_number = "Извини, непонятный номер книги :("
message_what_to_do = "Ты выбрал книгу - что с ней делать?"
message_suggest_cool = "Круто! Какую книгу хочешь предложить?"
message_thanks_for_suggest = "Спасибо! Твое пожелание зафиксировано"
message_suggest_prefix = "Новое предложение книги: "
message_stupid_bot = "Ты глупый"
message_stupid_bot_reply = "Это не мешает мне прекрасно справляться с моей работой!:)"
message_collection_forbidden = "Попытка коллекшена от неавторизованного юзера!!!"
message_collection_successfull = "Коллектед :)"
message_collection = "Добрый день. Извиняюсь за назойливость, но у нас принято брать книгу не больше чем на две недели. Пожалуйста, верните книгу номер {0} на полку, если не читаете ее"
message_healthcheck = "У меня все хорошо"

message_addbook_name = "Как называется книга?"
message_addbook_description = "Введи ссылку на описание с картинкой"
message_addbook_mistaken = "Непонятненько..."
message_addbook_success = "Всё круто!:)"
message_ping_reader = "Привет! Тут есть желающий на книгу номер {0}, которую ты читаешь :)"
message_ping_requester_successfull = "Отлично, читающий теперь знает, что книжка интересна не только ему :)"
message_ping_requester_unsuccessfull = "Кажется, книгу никто не читает. Должна быть на полке"
message_subscribe_successfull = "Отлично, после возврата книги тебе придет уведомление"
message_subscribe_returned = "Книга {0} вернулась на полку {1}!"

message_releasenotes_waiting = "Введите текст рассылки"
message_releasenotes_forbidden = "Попытка рассылки о релизе от неавторизованного юзера!!!"
message_releasenotes_successfull = "Успешно отправлены заметки о релизе"
message_releasenotes_problem = "Не удается доставить до пользователя {0}"

bookshelfs = ["17 этаж", "25 этаж"]
