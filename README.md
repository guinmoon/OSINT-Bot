# Пример Telegram OSINT бота
Пример OSINT бота с возможностью поиска по собсвенной БД так и в режиме реального времени с использованием запросов к интернет ресурсам. 

# Запуск
## Docker
Бот возможно запускать использую Docker
Необходимо создать файл config_docker.json, пример файла docker_config_sample.json
первый запуск: docker-compose -up -d build
последующие запуски: docker-compose -up

## Отладка в Visual Studio Code
В репозитории присутсвует директория .vscode с настройками для запуска

# Использование
h:<запрос> поиск по истории запросов
p:l<номер телефона> - поиск по номеру в локальной базе
p:o<номер телефона> - запрос в Ok.ru
p:f<номер телефона> - запрос в facebook.com (eyecon)
p:a<номер телефона> - поиск по номеру, все доступные варианты

t:#<идентификатор> - поиск по идентификатору Telegram в локальной базе
t:@<ник> - поиск по нику Telegram в локальной базе

s:o<идентификатор страницы> - поиск по странице в Одноклассниках
s:e<почтовый адрес> - поиск по адресу электронной почты
s:S:<o,v,a> <поисковый запрос>- поиск по соц сетям по заданым критериям
o - Ok, v - Vk, a - All
Пример: s:S:a q=Алина Балашова, a=18-30, city=москва

k:<ключевое слово>, поиск по ключевым словам, 
можно использовать MySQL FullText Search синтаксис 
https://valera.ws/2008.04.15~fulltext-in-mysql/, 
например +Александр +Смирнов найдет всех Александров Смирновых

Бот поддерживает последовательное выполнение запросов разделенных
знаком новой строки, однако запрос p:a запускается в паралельных
потоках и не понятно какой ответ относится к какому запросу
НЕОБХОДИМО ДОРАБОТАТЬ

## Модули грузки данных в локальну базу данных
Примеры загрузки различной информации расположена в директории insert_tool

## Написание модулей запросов к интернет ресурсам
Для добавления необходимо изучить структуру файлов:
    get_info_helpers.py - получиние информации
    info_parsers.py - формат представление информации в боте (не обязательно)
После написания функиции получения информации неоходимо добавить ее bot.py