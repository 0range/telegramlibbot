token = "341986347:AAFapU55A4CySynQWbPJNblDNebqcR2UCkI"

manager = 81593382
collection_time = 1209600

filename_status = "books_status.data"
filename_book_list = "book_list.json"
filename_log_name = "log"
filename_log_extension = ".log"

log_text = "name=\"{0}\" surname=\"{1}\" id={2} text=\"{3}\" answer=\"{4}\" \n"

message_start_bot = "Bot initialised"
message_start = """Привет! Я бот-библиотекарь в SME.
Скажи мне, какую книжку ты хочешь взять, и я тебя запишу ;)

Пообщаться со мной можно так:
/take - Взять книгу с полки
/return - Вернуть книгу на полку
/list - Посмотреть, что лежит на полке
/suggest - Предложить добавить книгу на полку

и, конечно
/help - Список команд"""
message_help =  """Напоминаю:
/take - Взять книгу с полки
/return - Вернуть книгу на полку
/list - Посмотреть, что лежит на полке
/suggest - Предложить добавить книгу

/help - Список команд"""
message_tell_book_number_get = "Скажи номер книги, которую хочешь взять"
message_tell_book_number_return = "Скажи номер книги, которую возвращаешь"
message_already_taken = "Кажется, эту книгу уже забрали"
message_you_got_book = "Отлично, книга номер {0} - {1} теперь у тебя"
message_already_returned = "Кажется, эта книга уже на полке"
message_you_returned_book = "Отлично, книга номер {0} - {1} вернулась на полку. Спасибо!"
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


lib = dict({
1: ["Алистер Коберн. Современные методы описания функциональных требований к системам","Как писать юз-кейсы https://www.ozon.ru/context/detail/id/5820242/",""],
2: ["Глеб Архангельский. Тайм-драйв","Как успевать жить и работать http://www.mann-ivanov-ferber.ru/books/mif/005/",""],
3: ["Михаил Литвак. Командовать или подчиняться","Психология управления http://www.labirint.ru/books/140103/",""],
4: ["Джефф Сазерленд. SCRUM","Революционный метод управления проектами http://www.mann-ivanov-ferber.ru/books/scrum/",""],
5: ["Девид Аллен. Как привести дела в порядок","Искусство продуктивности без стресса http://www.mann-ivanov-ferber.ru/books/mif/gettingthingsdone/",""],
6: ["Эрик Рис. Бизнес с нуля","Метод Lean Startup для быстрого тестирования идей и выбора бизнес-модели https://www.alpinabook.ru/catalog/StartupsInnovativeEntrepreneurship/65396/",""],
7: ["Ицхак Адизес. Идеальный руководитель","Почему им нельзя стать и что из этого следует https://www.alpinabook.ru/catalog/GeneralManagment/6609/",""],
8: ["Ицхак Адизес. Развитие лидеров","Как понять свой стиль управления и эффективно общаться с носителями иных стилей http://www.ozon.ru/context/detail/id/3725289/",""],
9: ["Олег Тиньков. Я такой как все","Автобиография основателя Тинькофф Банка https://www.ozon.ru/context/detail/id/31227508/",""],
10: ["Олег Тиньков. Я такой как все","Автобиография основателя Тинькофф Банка https://www.ozon.ru/context/detail/id/31227508/",""],
11: ["Ф.Брукс. Мифический человеко-месяц","Эта книга - юбилейное (дополненное и исправленное) издание своего рода библии для разработчиков программного обеспечения во всем мире www.ozon.ru/context/detail/id/83760/",""],
12: ["Г.Кеннеди. Договориться можно обо всем","Как добиваться максимума в любых переговорах https://www.alpinabook.ru/catalog/NegotiationsBusinessCommunication/66435/",""],
13: ["Эдуард Френкель. Любовь и математика","Сердце скрытой реальности https://www.ozon.ru/context/detail/id/32224115/ \nP.S. Эта книга на полке букшеринга, то есть принадлежит кому-то из команды",""],
14: ["Stephen Few. Information dashboard design","Пособие по эффективной визуализации (на английском) https://www.amazon.com/Information-Dashboard-Design-Effective-Communication/dp/0596100167 \nP.S. Эта книга на полке букшеринга, то есть принадлежит кому-то из команды",""],
15: ["Джин Желязны. Говори на языке диаграм","Пособие по визуальным коммуникациям http://www.mann-ivanov-ferber.ru/books/mif/026/ \nP.S. Эта книга на полке букшеринга, то есть принадлежит кому-то из команды",""],
16: ["Essetial Kanban Condensed","Краткое пособие по Kanban от автора полного пособия http://leankanban.com/guide/",""],
17: ["Хенрик Книберг. Scrum и XP: заметки с передовой","Рассказ о том, как строится скрам в одной компании http://agilerussia.ru/books/scrum_xp-from-the-trenches/",""],
18: ["Генри Форд. Моя жизнь, мои достижения","Автобиография великого Генри Форда. Рекомендована Олегом Тиньковым http://www.mann-ivanov-ferber.ru/books/history/my-life-and-work/",""],
19: ["Олег Тиньков. Как стать бизнесменом","Вторая книга основателя Тинькофф Банка http://www.mann-ivanov-ferber.ru/books/paperbook/kak-stat-biznesmenom/",""],
20: ["В.Чан Ким, Рене Моборн. Стратегия голубого океана","Как найти или создать рынок, свободный от других игроков http://www.mann-ivanov-ferber.ru/books/paperbook/blueoceanstrategy/",""],
21: ["Роман Пихлер. Управление продуктом в SCRUM","Руководство по гибкому управлению продуктом на основе Scrum — от одного из ведущих экспертов по методике http://www.mann-ivanov-ferber.ru/books/upravlenie-produktom-v-scrum/",""],
22: ["Бретт Кинг. Банк 3.0","Банку будущего. Почему сегодня банк - это не то, куда вы ходите, а то, что вы делаете. http://www.ozon.ru/context/detail/id/30453749/",""],
23: ["Фредерик Лалу. Открывая организации будущего","Принципиально новый взгляд на развитие организаций, который поможет перейти на следующий уровень развития и построить сознательную и цельную компанию будущего. http://www.mann-ivanov-ferber.ru/books/novyj-vzglyad-na-organizacii/",""],
24: ["Максим Богатырев. 45 татуировок продавана","Правила для тех, кто продаёт и управляет продажами http://www.mann-ivanov-ferber.ru/books/tatuirovki-prodavana/",""],
25: ["Максим Богатырев. 45 татуировок менеджера","Правила российского руководителя http://www.mann-ivanov-ferber.ru/books/paperbook/tattoos/",""]
})
