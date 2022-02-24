#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BotFather, [2/22/22 17:28]
# Alright, a new bot. How are we going to call it? Please choose a name for your bot.

# Вероника *********, [2/22/22 17:29]
# spider0sintb0t

# BotFather, [2/22/22 17:29]
# Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.

# Вероника *********, [2/22/22 17:29]
# spider0sint_bot

# BotFather, [2/22/22 17:29]
# Done! Congratulations on your new bot. You will find it at t.me/spider0sint_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 5268778142:AAEGVBkzPJ85KSThJ7fCTOEVCvRZoe5ueqk
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
"""

"""

import logging
import postgres_helper
# import pymysql
from sqlalchemy import create_engine
import json
import argparse
import re
import time
import threading
import os
import subprocess
import requests
import copy

from lxml import html
from datetime import datetime
from setproctitle import setproctitle

import vk_api
import vk_api_helper
import ok_api

from get_info_helpers import *
from info_parsers import *


# from getcontact.getcontact import GetContactAPI

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telegram.utils import helpers


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

Config = []

# Используются в модуле numbuster
proxies = {
    'http': 'socks5://193.187.173.216:5586',
    'https': 'socks5://193.187.173.216:5586'
}

# для запросов на поиск страниц ВК
vk_session = []

logger = logging.getLogger(__name__)
connection = []

# Гет выдает капчу, для обхода используется платный сервис https://anti-captcha.com/
getcontact = None
try:
    getcontact = GetContactAPI(
        anticaptcha_key=Config['anticaptcha_key'], manual_captcha_decode=Config['get_contact_manual_captcha'], proxies=proxies)
except Exception as exccc:
    print(str(exccc))

# Тут будут храниться идентификаторы интерактивных запросов (с кнопками)
# чтоб моудль ответов знал на какой запрос он отвечает
Queries = ['']*87000

help_message = """h:<запрос> поиск по истории запросов
p:l<номер телефона> - поиск по номеру в локальной базе
[EROOR] p:n<номер телефона> - запрос в Numbuster 
[ERROR] p:g<номер телефона> - запрос в Getcontact
p:o<номер телефона> - запрос в Ok.ru
p:f<номер телефона> - запрос в facebook.com (eyecon)
[ERROR 523]p:m<номер телефона> - запрос в mirror.bullshit.agency
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
"""


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def log_message(message, message_text, response=None, write_log=True):
    text = message_text.replace('"', '')
    from_user = message["from_user"]
    chat_id = message["chat_id"]
    from_user_id = str(from_user["id"])
    from_user_nick = str(from_user["username"])
    from_user_name = str(from_user.full_name)
    text = text.replace("'", "")
    query = ''
    if response is None:
        query = "insert into telebot_log (from_user_id,from_user_nick,from_user_name,message) values "
        query += "(%s,'%s','%s','%s')" % (from_user_id,
                                          from_user_nick, from_user_name, text)
    else:
        response = response.replace("'", "")
        response = response.replace('"', '')
        response = response.replace('\\', '')
        query = "insert into telebot_log_responses (from_user_id,from_user_nick,from_user_name,message,response_text) values "
        query += "(%s,'%s','%s','%s','%s')" % (from_user_id,
                                               from_user_nick, from_user_name, text, response)
    if Config["log"] and write_log == True:
        postgres_helper.db_import(connection, query)
        # query = "update telebot_white_list set chat_id=%s where user_id=%s"%(chat_id,from_user_id)
        # postgres_helper.db_import(connection, query)

    return from_user_id


# Бот отвечает только пользователям id которых есть в таблице telebot_whitelist
# Остальным бот отвечает тем же сообщением что прислал пользователь
def check_user_whitelist(from_user_id):
    query = "select id from telebot_whitelist where user_id = %s" % from_user_id
    res = postgres_helper.db_select_one(connection, query)
    if(res is not None):
        return True
    else:
        return False


# Генератор случайных id для Queries
def get_uniq_id():
    now = datetime.now()
    seconds_since_midnight = (
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds
    return seconds_since_midnight


def parse_message(update, context, force_message=None):
    # """Echo the user message."""
    # reply = "\nAnastasia Deryabina\nhttps://vk.com/id14224576\n[inline URL](https://sun1-24.userapi.com/impg/iReoL5X8wiX1ScMkR2K_APK8LYGd3A_5D-u0UA/b3hBYXmvmKQ.jpg?size=200x0&quality=88&crop=1023,180,959,959&sign=4e824479e48c12fcfdd1b2300457b66d&c_uniq_tag=Vk37V3pbZf7s3R0ufTEJ64oxVbmR2VRdCrlNj-22Hwg&ava=1)"
    # reply = "hello\n[inline URL](https://vk.com/id14224576)"
    # update.message.bot.send_message(update.message.chat.id,reply,"MarkdownV2")
    # return
    text_raw = update.message.text
    if force_message is not None:
        text_raw = force_message
    print(text_raw)
    if not hasattr(update, 'is_from_another_parser'):
        from_user_id = log_message(update.message, text_raw)
    else:
        from_user_id = log_message(update.message, text_raw, write_log=False)
    response = {"parse_mode": "MarkdownV2",
                "info": helpers.escape_markdown(update.message.text, version=2)}
    reply_menu = False
    menu_text = ""
    if not hasattr(update, 'is_from_another_parser'):
        if not check_user_whitelist(from_user_id):
            update.message.reply_text(
                response["info"], parse_mode=response["parse_mode"])
            return
    text_multiline = text_raw.split('\n')

    # Бот поддерживает последовательное выполнение запросов разделенных
    # знаком новой строки, однако запрос p:a запускается в паралельных
    # потоках и не понятно какой ответ относится к какому запросу
    # НЕОБХОДИМО ДОРАБОТАТЬ

    for text in text_multiline:
        try:
            if len(text_multiline) > 1:
                update.message.reply_text("Запрос %s" % text)
            if text[:5] == "help:":
                response = {"parse_mode": "", "info": help_message}
            if text[:2] == "a:":
                response["info"] = "admin response: "
                admin_query = text[2:]
                if admin_query[:1] == "a":
                    a = 1
                    # send_to_all
            if text[:2] == "h:":
                response["info"] = "history info: "
                history_query = text[2:]
                response = get_info_by_history(history_query, connection)
            if text[:2] == "t:":
                response["info"] = "telegram info: "
                telegram_query = text[2:]
                if telegram_query[:1] == "#":
                    telegram_query_uid = telegram_query[1:]
                    if re.match("^[0-9]*$", telegram_query_uid):
                        response = get_telegram_info_by_uid(
                            telegram_query_uid, connection)
                    else:
                        response["info"] = "incorrect"
                    response["info"] += telegram_query_uid
                if telegram_query[:1] == "@":
                    telegram_query_nick = telegram_query[1:]
                    if re.match("^[A-Za-z0-9_-]*$", telegram_query_nick):
                        response = get_telegram_info_by_nick(
                            telegram_query_nick, connection)
                    else:
                        response["info"] = 'Invalid nick name'
            if text[:2] == "p:":
                response["info"] = "phone info: "
                phone_query = text[2:]
                phone_num = phone_query[1:]
                if not re.match("^[0-9]*$", phone_num):
                    response["info"] += 'Invalid phone number'
                else:
                    if not hasattr(update, 'is_from_another_parser'):
                        update.message.reply_text("Ваш запрос обрабатывается")
                    if phone_query[:1] == "l":
                        response = get_info_by_phone_local(
                            phone_num, connection)
                    if phone_query[:1] == "o":
                        response = get_info_by_phone_ok(phone_num)
                        if "json" in response:
                            query_data = '[oksamevk]:'+response["json"]
                            seconds_since_midnight = get_uniq_id()
                            Queries[seconds_since_midnight] = query_data
                            keyboard = [[InlineKeyboardButton(
                                "Вконтакте", callback_data=seconds_since_midnight)]]
                            reply_menu = InlineKeyboardMarkup(keyboard)
                            menu_text = 'Искать похожие в:'
                    if phone_query[:1] == "n":
                        response = get_info_by_phone_numbuster(
                            phone_num, Config["numbuster_token"])
                    if phone_query[:1] == "g":
                        response = get_info_by_phone_getcontact(
                            phone_num, getcontact)
                    if phone_query[:1] == "f":
                        response = get_info_by_phone_facebook(phone_num)
                    if phone_query[:1] == "m":
                        response = get_info_by_bullshit_agency(
                            phone_num, proxies)
                    if phone_query[:1] == "a":
                        query = "%s" % phone_num
                        res = get_info_by_history(
                            query, connection, check_only=True)
                        if res["len"] > 0 and not hasattr(update, 'is_from_another_parser'):
                            query_data_history = '[history]:'+query
                            seconds_since_midnight_ghunt = get_uniq_id()
                            Queries[seconds_since_midnight_ghunt] = query_data_history
                            query_data_phone_all = '[query_data_phone_all]:'+query
                            seconds_since_midnight_breachcompilation = get_uniq_id()+1
                            Queries[seconds_since_midnight_breachcompilation] = query_data_phone_all
                            keyboard = [[InlineKeyboardButton("Отобразить историю", callback_data=seconds_since_midnight_ghunt), InlineKeyboardButton(
                                "Искать заново", callback_data=seconds_since_midnight_breachcompilation)]]
                            menu_text = 'В истории запросов содержится информация о текущем номере:'
                            reply_menu = InlineKeyboardMarkup(keyboard)
                            response["info"] = "Найдено в истории"
                        else:
                            update.is_from_another_parser = property(
                                lambda self: True)
                            update.from_another_parser_count = property(
                                lambda self: True)
                            update.from_another_parser_count = 0
                            new_message = "p:l"+phone_num
                            threading.Thread(target=parse_message, args=[
                                             update, context, new_message]).start()
                            # new_message = "p:n"+phone_num
                            # threading.Thread(target=parse_message, args=[
                            #                  update, context, new_message]).start()
                            # new_message = "p:g"+phone_num
                            # threading.Thread(target=parse_message,args=[update,context,new_message]).start()
                            # new_message = "p:m"+phone_num
                            # threading.Thread(target=parse_message, args=[
                            #                  update, context, new_message]).start()
                            new_message = "p:o"+phone_num
                            threading.Thread(target=parse_message, args=[
                                             update, context, new_message]).start()
                            new_message = "p:f"+phone_num
                            threading.Thread(target=parse_message, args=[
                                             update, context, new_message]).start()
                            continue
                    if hasattr(update, 'from_another_parser_count'):
                        update.from_another_parser_count += 1
                        if update.from_another_parser_count == 3:
                            response["info"] += "\n\n🏁🏁🏁 Выполнение запроса завершено 🏁🏁🏁"
            if text[:2] == "k:":
                response["info"] = "keyword info: "
                keyword_query = text[2:]
                if re.match("^[A-Za-z0-9А-Яа-я+><*\" _-]*$", keyword_query) and len(keyword_query) >= 3 and len(keyword_query) <= 50:
                    update.message.reply_text("Ваш запрос обрабатывается")
                    response = get_info_by_keyword(
                        keyword_query, connection, False)
                    if response["len"] > 3:
                        query_data = '[report]k:'+keyword_query
                        now = datetime.now()
                        seconds_since_midnight = (
                            now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds
                        Queries[seconds_since_midnight] = query_data
                        keyboard = [[InlineKeyboardButton(
                            "Полный отчет", callback_data=seconds_since_midnight)]]
                        reply_menu = InlineKeyboardMarkup(keyboard)
                        menu_text = 'Отображены первые 3 результата:'

                else:
                    response["info"] += 'Incorrect Keyword or len'
            if text[:2] == "s:":
                response["info"] = "social info: "
                social_query = text[2:]
                if not re.match("^[A-Za-z0-9А-Яа-я+><*\"@. _-]*$", text[2:]) and social_query[:1] != "S":
                    response["info"] += 'Invalid social id'
                else:
                    if not hasattr(update, 'is_from_another_parser'):
                        update.message.reply_text("Ваш запрос обрабатывается")
                    if social_query[:1] == "o":
                        response = get_info_by_ok_url_uid(
                            social_query[1:], connection)
                    if social_query[:1] == "e":
                        email = social_query[1:]
                        response = get_info_by_email(email, connection)
                        # if email.find("@gmail")>0:
                        query_data_ghunt = '[ghunt]:'+email
                        seconds_since_midnight_ghunt = get_uniq_id()
                        Queries[seconds_since_midnight_ghunt] = query_data_ghunt
                        query_data_breachcompilation = '[breachcompilation]:'+email
                        seconds_since_midnight_breachcompilation = get_uniq_id()+1
                        Queries[seconds_since_midnight_breachcompilation] = query_data_breachcompilation
                        keyboard = [[InlineKeyboardButton("GHunt", callback_data=seconds_since_midnight_ghunt), InlineKeyboardButton(
                            "BreachCompilation", callback_data=seconds_since_midnight_breachcompilation)]]
                        reply_menu = InlineKeyboardMarkup(keyboard)
                        menu_text = 'Информация email:'
                    if social_query[:1] == "S":
                        full_query = social_query[2:]
                        fname = ""
                        soup_query = full_query[1:]
                        if full_query[:1] == "o":
                            fname = get_info_by_soup_query(
                                soup_query, "ok", Config, vk_session)
                        if full_query[:1] == "v":
                            fname = get_info_by_soup_query(
                                soup_query, "vk", Config, vk_session,)
                        if os.path.exists(fname) and full_query[:1] != "a":
                            f = open(fname, "rb")
                            update.message.bot.send_document(
                                update.message.chat.id, f)
                        if not os.path.exists(fname) and full_query[:1] != "a":
                            update.message.reply_text("Не найдено.")
                        if full_query[:1] == "a":
                            update.is_from_another_parser = property(
                                lambda self: True)
                            update.message.text = "s:S:v"+soup_query
                            parse_message(update, context)
                            update.message.text = "s:S:o"+soup_query
                            parse_message(update, context)
                            continue
                        if full_query[:1] != "a":
                            response["info"] = "🏁🏁🏁 Выполнение запроса завершено 🏁🏁🏁"
                        a = 1
        except Exception as expt:
            response = str(expt)
        response_data = response
        response_parse_mode = None
        if "info" in response:
            response_data = response["info"]
        if "parse_mode" in response:
            response_parse_mode = response["parse_mode"]
        if len(response_data) > 4096:
            response_data = response_data[:4095]
        update.message.reply_text(
            response_data, parse_mode=response_parse_mode)
        try:
            log_message(update.message, text, response_data)
        except Exception as expt:
            print(str(expt))
        if reply_menu != False:
            update.message.reply_text(menu_text, reply_markup=reply_menu)


# """
# Тут происходит ответ на интерактивные нажатия (кнопки)
# """
def report(update, context):
    query = update.callback_query
    query.answer()
    text = Queries[int(query.data)]
    if text.find("[report]k:") == 0:
        response = "keyword info: "
        keyword_query = text[10:]
        query.edit_message_text("Выполняется построение отчета")
        response = get_info_by_keyword(keyword_query, connection, True)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fname = "reports/report%s.txt" % timestr
        report_file = open(fname, "wt")
        n = report_file.write(response["info"])
        report_file.close()
        f = open(fname, "rb")
        query.bot.send_document(query.message.chat.id, f)
    if text.find("[oksamevk]:") == 0:
        user = json.loads(text[11:])["users"][0]
        vk_query = {"q": "%s %s" % (user["first_name"], user["last_name"])}
        vk_query["count"] = 5
        vk_query["fields"] = "photo,screen_name,photo_200"
        if "location" in user and "city" in user["location"]:
            vk_query["city"] = user["location"]["city"]
        if "age" in user:
            vk_query["age_from"] = user["age"]
            vk_query["age_to"] = user["age"]
        query.edit_message_text("Выполняется поиск подходящих профилей")
        vk_profiles = vk_api_helper.vk_search_same(vk_session, vk_query)
        pretty_vk_profiles = parse_vk_info(vk_profiles)
        query.bot.send_message(
            query.message.chat.id, pretty_vk_profiles["info"], pretty_vk_profiles["parse_mode"])
        # query.edit_message_text(pretty_vk_profiles["info"])
    if text.find("[ghunt]:") == 0:
        email = text[8:]
        query.bot.send_message(query.message.chat.id,
                               "Выполняется поиск информации...")
        email_info = ghunt_info(email, Config['debug'])
        query.bot.send_message(
            query.message.chat.id, email_info["info"], parse_mode=email_info["parse_mode"])
    if text.find("[breachcompilation]:") == 0:
        email = text[20:]
        query.bot.send_message(query.message.chat.id,
                               "Выполняется поиск информации...")
        email_info = breachcompilation_info(email, Config['debug'])
        query.bot.send_message(
            query.message.chat.id, email_info["info"], parse_mode=email_info["parse_mode"])
    if text.find("[history]:") == 0:
        hquery = text[10:]
        response = get_info_by_history(hquery, connection)
        if len(response["info"]) > 4096:
            response["info"] = response["info"][:4000] + \
                "'\n🔪 🔪 🔪 🔪 ОБРЕЗАНО🔪 🔪 🔪 🔪 "
        query.bot.send_message(
            query.message.chat.id, response["info"], parse_mode=response["parse_mode"])
    if text.find("[query_data_phone_all]:") == 0:
        hquery = text[23:]
        hquery = 'p:a%s' % hquery
        update.is_from_another_parser = property(lambda self: True)
        update.message = query.message
        update.message.text = hquery
        parse_message(update, context)


def main():
    """Start the bot."""
    updater = Updater(Config['bot_token'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(report))
    dp.add_handler(MessageHandler(Filters.text & ~
                                  Filters.command, parse_message))

    updater.start_polling()
    updater.idle()


def reconnect_function(timeout):
    time.sleep(timeout)
    global connection
    try:
        connection.close()
    except Exception as expt:
        print(str(expt))
    engine = create_engine('postgresql+psycopg2://'+Config['db_user']+':' +
                           Config['db_password'] + '@' + Config['db_address']+':'+str(Config['db_port']) + '/' + Config['db_name'])
    connection = engine.connect()
    print("Reconected.")


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=('Strat bot option'),
    )
    parser.add_argument('--config',  required=False, default='config.json', type=str,
                        help='config path')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    setproctitle("spider0sint_bot")

    args = parse_args()

    with open(args.config, 'r') as f:
        Config = json.load(f)
        Config = Config['configuration']

    engine = create_engine('postgresql+psycopg2://'+Config['db_user']+':' +
                           Config['db_password'] + '@' + Config['db_address']+':'+str(Config['db_port']) + '/' + Config['db_name'])
    connection = engine.connect()
    vk_session = vk_api.VkApi(Config['vk_user_name'], Config['vk_password'])

    if Config['use_vk']:
        vk_session.auth()

    # reconnect_thread = threading.Thread(
    #     target=reconnect_function, args=(3600,))
    # reconnect_thread.start()
    main()
