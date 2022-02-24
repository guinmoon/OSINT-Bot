from telegram.utils import helpers
# import pymysql
import os
import requests

import econ_api
import NumbusterAPI

# import postgres_helper
import postgres_helper
from info_parsers import *
import vk_api_helper
import ok_api


def get_info_by_phoneid(phone_id, connection):
    query = "select phone,info,type,uid from phones_info_parsed join phones on phones_info_parsed.phone_id=phones.id join ref_phone_info_types on ref_phone_info_types.id=phones_info_parsed.info_type  where phone_id=" + \
        str(phone_id[0])
    res = postgres_helper.db_select_many(connection, query)
    pretty_info = ''
    if len(res) > 0:
        pretty_info = "\n\n📞 Тел. "+res[0][0]+":"
    for phone_info in res:
        phone_info_pretty = phone_info[1]
        info_type_pretty = phone_info[2]
        pre = '\n'
        if phone_info[2] == 'Numbuster':
            phone_info_pretty = parse_numbuster_local(phone_info[1])
            info_type_pretty = '✆'+info_type_pretty
        if phone_info[2] == 'Telegram':
            info_type_pretty = '💬 %s: id%s' % (info_type_pretty, phone_info[3])
        if phone_info[2] == "vk100m":
            phone_info_pretty = parse_vk100m_info_cerebro(phone_info[1])
        if phone_info[2] == "avito.ru":
            phone_info_pretty = parse_avito_info_cerebro(phone_info[1])
        if phone_info[2] != "Ok.ru":
            pretty_info += "%s%s: %s" % (pre,
                                         info_type_pretty, phone_info_pretty)

    # pretty_info = helpers.escape_markdown(pretty_info,version=2)
    # info = {"parse_mode":"MarkdownV2","info":pretty_info}
    info = pretty_info
    return info


def get_info_by_phone_local(phone, connection):
    pretty_info = "Not Found"
    # uid='173004422'
    query = "select id from phones where phone='"+phone+"'"
    result = postgres_helper.db_select_many(connection, query)
    for phone_id in result:
        pretty_info = get_info_by_phoneid(phone_id, connection)
    pretty_info = "\n🗄 Local 🗄"+pretty_info
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def get_info_by_phone_numbuster(phone, token):
    pretty_info = 'phone not found'
    # uid='173004422'
    pretty_info = NumbusterAPI.get_numbuster_info(
        phone, token, use_tor=False, renew_ip=False, use_proxy=True)
    pretty_info = '📞 Numbuster Запрос\n'+parse_numbuster(pretty_info)
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def get_telegram_info_by_uid(uid, connection):
    pretty_info = 'id not found'
    query = "select phone_id from phones_info_parsed where info_type=2 and uid=%s" % uid
    result = postgres_helper.db_select_many(connection, query)
    for phone_id in result:
        pretty_info = get_info_by_phoneid(phone_id, connection)
        # pretty_info = get_info_by_phoneid(phone_id)["info"]
    pretty_info = helpers.escape_markdown(pretty_info, version=2)
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    return info


def get_telegram_info_by_nick(nick, connection):
    pretty_info = 'nick not found'
    # uid='173004422'
    query = "select phone_id from phones_info_parsed where info_type=2 and info like '["+nick+"%%'"
    result = postgres_helper.db_select_many(connection, query)
    if len(result) > 0:
        pretty_info = ''
    for phone_id in result:
        pretty_info += get_info_by_phoneid(phone_id, connection)
        # pretty_info += get_info_by_phoneid(phone_id)["info"]
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


# Update [01.01.2022]
# GetContact changed API, therefore project is not working. Maybe in future will be fixed

# def get_info_by_phone_getcontact(phone, getcontact):
#     # uid='173004422'
#     pretty_info = ''
#     if getcontact is None:
#         pretty_info = 'Getcontact TOKEN Error.'
#     else:
#         pretty_info = getcontact.get_information_by_phone(phone)
#         pretty_info = '📞 GetContact Запрос\n'+parse_getcontact(pretty_info)
#     info = {"parse_mode": "MarkdownV2", "info": pretty_info}
#     info["info"] = helpers.escape_markdown(info["info"], version=2)
#     return info


def get_info_by_phone_facebook(phone):
    # uid='173004422'
    pretty_info = econ_api.facebook_by_phone(phone)
    pretty_info = '📞EYECon Запрос\n'+parse_eyecon(str(pretty_info))
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def get_info_by_phone_ok(phone):
    info = {"parse_mode": "MarkdownV2", "info": "Not Found"}
    stream = os.popen(
        'cd ok_tools && node ./profile_by_phonenumber.js %s true' % phone)
    raw_info = stream.read()
    # print(raw_info)
    # raw_info = '{"users":[{"uid":"293479657422","birthday":"1994-10-18","birthdaySet":true,"age":26,"first_name":"моногаров","last_name":"максим","gender":"male","location":{"city":"с.Константиновское","country":"RUSSIAN_FEDERATION","countryCode":"RU","countryName":"Russia"},"pic128x128":"https://api.ok.ru/img/stub/user/male/128.png","pic600x600":"https://api.ok.ru/img/stub/user/male/600.png","url_profile":"https://ok.ru/profile/522179841083"}]}\n'
    info["info"] = parse_ok_info(raw_info)
    info["info"] = '📞 Oknoklassniki Запрос:\n'+info["info"]
    if raw_info != "false\n":
        info["json"] = raw_info
    return info


def get_info_by_keyword(keywords_str, connection, full_result=False):
    pretty_info = 'keyword not found'
    # uid='173004422'
    # keywords = keywords_str.split("+")
    # query = "select phone_id from phones_info_parsed where 1=1 "
    # for keyword in keywords:
    #     query += " and info like '%"+keyword+"%'"
    query = 'SELECT phone_id,info,info_type FROM phones_info_parsed WHERE MATCH(info) AGAINST(\'%s\' IN BOOLEAN MODE)' % keywords_str
    if not full_result:
        query += " limit 4"
    result = postgres_helper.db_select_many(connection, query)
    if len(result) > 0:
        pretty_info = ''
    max_res_count = 3
    for phone_data in result:
        if not full_result and max_res_count <= 0:
            break
        pretty_info += get_info_by_phoneid(phone_data, connection)
        if phone_data[2] == 3:
            pretty_info += '\n%s' % parse_ok_info_cerebro(phone_data[1])
        max_res_count -= 1

    info = {"parse_mode": "MarkdownV2",
            "info": pretty_info, "len": len(result)}
    if not full_result:
        info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def get_info_by_ok_url_uid(ok_uid, connection):
    markdownv2_info = "not found"
    query = "select * from phones_info_parsed where info like '" + \
        str(ok_uid)+"%'"
    result = postgres_helper.db_select_many(connection, query)
    if len(result) > 0:
        markdownv2_info = "\nid[%i](https://ok.ru/profile/%s)" % (
            result[0][3], ok_uid)
        query = "select phone from phones where id=%i" % result[0][1]
        phone = postgres_helper.db_select_one(connection, query)
        phone = helpers.escape_markdown(phone[0], version=2)
        markdownv2_info += "\n%s" % phone
    info = {"parse_mode": "MarkdownV2", "info": markdownv2_info}
    return info


def get_info_by_email(email, connection):
    pretty_info = 'email not found'
    query = 'SELECT phone_id FROM phones_info_parsed WHERE info = \'%s\'' % email
    result = postgres_helper.db_select_many(connection, query)
    if len(result) > 0:
        pretty_info = '📨 Email:\n'
    for phone_id in result:
        pretty_info += get_info_by_phoneid(phone_id, connection)
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def ghunt_info(email, debug):
    info = {"parse_mode": "MarkdownV2", "info": "Not Found"}
    cmd = 'cd /home/m_vs_m/cerebro/addons/GHunt && python3 ./hunt_json.py %s' % email
    if debug:
        cmd = 'cd /Volumes/D/dev/GHunt && python3 ./hunt_json.py %s' % email
    stream = os.popen(cmd)
    raw_info = stream.read()
    # raw_info='[+] 1 account found !\n\n------------------------------\n\nName: Bijuteriya Bishkek\n\nLast profile edit : 2019/10/22 10:59:05 (UTC)\n\nEmail : samsalieva.elmira@gmail.com\nGoogle ID : 103686898554671034208\n\nHangouts Bot : No\n\nActivated Google services :\n- Youtube\n- Photos\n- Maps\n\nYouTube channel (confidence => 90.0%) :\n- [Bijuteriya Bishkek] https://youtube.com/channel/UCIi7wP9WnGvNVyiIVylXNkA\n\nGoogle Maps : https://www.google.com/maps/contrib/103686898554671034208/reviews\nInitial request...\nStarting browser...\nSetting cookies... \nFetching reviews page...\n=> 1 reviews found !             \nFetching reviews... (1/1)\nFetching internal requests history...\nFetching internal requests... (0/0)  \nFetching reviews location... (0/1)   \nFetching reviews location... (1/1)   \nCalculation of the distance of each review...\nCalculation of the distance of each review (0/1)...\n                                                   \nIdentification of redundant areas...               \nCalculating confidence...                          \n                                                   \nProbable location (confidence => Very low) :\n- 宜野湾市, 日本 (Japan)\n'
    info["info"] = '📨 GHunt Запрос\n'+raw_info
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def breachcompilation_info(email, debug):
    info = {"parse_mode": "MarkdownV2", "info": "Not Found"}
    cmd = '/home/m_vs_m/cerebro/BreachCompilation/query.sh %s' % email
    if debug:
        cmd = 'echo %s' % email
    stream = os.popen(cmd)
    raw_info = stream.read()
    # raw_info='[+] 1 account found !\n\n------------------------------\n\nName: Bijuteriya Bishkek\n\nLast profile edit : 2019/10/22 10:59:05 (UTC)\n\nEmail : samsalieva.elmira@gmail.com\nGoogle ID : 103686898554671034208\n\nHangouts Bot : No\n\nActivated Google services :\n- Youtube\n- Photos\n- Maps\n\nYouTube channel (confidence => 90.0%) :\n- [Bijuteriya Bishkek] https://youtube.com/channel/UCIi7wP9WnGvNVyiIVylXNkA\n\nGoogle Maps : https://www.google.com/maps/contrib/103686898554671034208/reviews\nInitial request...\nStarting browser...\nSetting cookies... \nFetching reviews page...\n=> 1 reviews found !             \nFetching reviews... (1/1)\nFetching internal requests history...\nFetching internal requests... (0/0)  \nFetching reviews location... (0/1)   \nFetching reviews location... (1/1)   \nCalculation of the distance of each review...\nCalculation of the distance of each review (0/1)...\n                                                   \nIdentification of redundant areas...               \nCalculating confidence...                          \n                                                   \nProbable location (confidence => Very low) :\n- 宜野湾市, 日本 (Japan)\n'
    info["info"] = '📨 BreachCompilation Запрос\n'+raw_info
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info


def get_info_by_bullshit_agency(phone, proxies):  # Error 523
    url = "https://mirror.bullshit.agency/search_by_phone/+%s" % phone
    payload = {}
    # headers = {'Cookie': '__cfduid=dfbee79bb1b9f32e6d504fb4eba55ba111605516757; _mirror_session=QXpvRGpzVTdPT3VETmJZQUR3TmNoaUJhV3RJMVRRVXVBbHBHdWtwUHlra0NiWm95UERXRWlaOUxueDgyU1NRalZhSGpESUJyZGNjRnNQZXl6aitqTHZvdFhONmZYSk96QXVGcURORUZuL083OFNwajZoQTJvMWc0em9qa0pZbzNWZmVuRTd3WWFtMjdNT01CZTJzcHdBPT0tLTJxOS93Q1NUakxpVEhvcG5KUXNqZWc9PQ%3D%3D--d9d9a7c6ba05422645e54124e2aedee6c18684ec'}
    headers = {}
    # proxies = None
    response = requests.request(
        "GET", url, headers=headers, data=payload, proxies=proxies)
    pretty_info = response.text
    # pretty_info = '<!DOCTYPE html>\n<html lang="ru">\n  <head>\n    <meta charset="utf-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>  2 объявления по телефону +7 999 653-90-80\n</title>\n      <meta name="description" content="iPhone X 256GB (Ставропольский край, р-н Ленинский, улица Ленина, 31) | iPhone 6 128 GB обмен (Ставропольский край, Ставрополь, р-н Ленинский)"/>\n    <meta name="csrf-param" content="authenticity_token" />\n<meta name="csrf-token" content="J+ixPkrngS/yOY80ZW+YkDZHGbkOb8WYxb/jqnVP2qI9mUMG3AFmy5CcbJFVARMtveaeAzJpGYmYGIGtpqXFQg==" />\n\n    <link rel="stylesheet" media="all" href="/assets/application-e212689a75b4210b3de7d9c014e268ece8f1466ca44e900cbd61c9edf76170fd.css" />\n\n    <script src="/assets/application-b708f567506a926f536636fc4b2f226ffcff37302e504c85af1fdc02faf5a990.js"></script>\n\n    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->\n    <!--[if lt IE 9]>\n    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.2/html5shiv.min.js" type="text/javascript"></script>\n    <![endif]-->\n\n    <meta name="referrer" content="no-referrer" />\n\n          <script async src="https://yastatic.net/pcode/adfox/header-bidding.js"></script>\n      <script type="text/javascript" src="https://ads.digitalcaramel.com/js/bullshit.agency.js"></script>\n      <script src="https://yastatic.net/pcode/adfox/loader.js" crossorigin="anonymous"></script>\n\n\n  </head>\n  <body>\n\n    <div class="container">\n\n      \n        \n\n<div class="page-header">\n  <h1>2 объявления по номеру +79996539080</h1>\n</div>\n\n<form action="/search_by_phone" method="get" class="form-horizontal">\n  <div class="form-group">\n    <label for="phone" class="col-sm-4 control-label">Номер:</label>\n    <div class="col-sm-8">\n      <input type="text" name="phone" id="phone" value="+79996539080" placeholder="в любом формате, вообще в любом" class="form-control" />\n    </div>\n  </div>\n  <div class="form-group">\n    <div class="col-sm-offset-4 col-sm-8">\n      <button type="submit" class="btn btn-default">Искать в объявлениях на Авите</button>\n    </div>\n  </div>\n</form>\n\n\n  <div style="margin-bottom: 2em; maring-top: 1em">\n    <div id="adfox_1590332198983810000"></div>\n    <script>\n        window.Ya.adfoxCode.createAdaptive({\n            ownerId: 260971,\n            containerId: \'adfox_1590332198983810000\',\n            params: {\n                p1: \'cksit\',\n                p2: \'fsgt\'\n            }\n        }, [\'desktop\'], {\n            tabletWidth: 830,\n            phoneWidth: 480,\n            isAutoReloads: false\n        });\n    setInterval(function(){ \n                window.Ya.adfoxCode.reload(\'adfox_1590332198983810000\')\n    }, 30000);\n    </script>\n\n    <div id="adfox_159033219518376108"></div>\n    <script>\n        window.Ya.adfoxCode.createAdaptive({\n            ownerId: 260971,\n            containerId: \'adfox_159033219518376108\',\n            params: {\n                p1: \'cksiu\',\n                p2: \'fsgt\'\n            }\n        }, [\'phone\'], {\n            tabletWidth: 830,\n            phoneWidth: 480,\n            isAutoReloads: false\n        });\n    setInterval(function(){ \n                window.Ya.adfoxCode.reload(\'adfox_159033219518376108\')\n    }, 30000);\n    </script>\n  </div>\n\n<div class="row row-eq-height">\n  <div class="col-sm-8">\n          <a href="/ads/5af86122-254f-44db-93b0-1672f08dbfb4" rel="nofollow">\n  <div style="position: relative; min-height: 87px; vertical-align: baseline">\n    <div style="width: 115px; height: 75px; vertical-align: baseline; float: left">\n        <img src="https://img.avito.link/100x75/5587829023.jpg" alt="" style="max-width: 100px; max-height: 75px" />\n    </div>\n    <div style="vertical-align: baseline">\n      <h4 class="media-heading">iPhone X 256GB</h4>\n      <p>\n        <span class="text-muted">Ставропольский край, р-н Ленинский, улица Ленина, 31</span>\n        <br /><span class="text-muted">14 мая 2019\n      </p>\n    </div>\n  </div>\n  </a>\n      <a href="/ads/1d18ae5d-9e67-4261-9671-4069c4b8872f" rel="nofollow">\n  <div style="position: relative; min-height: 87px; vertical-align: baseline">\n    <div style="width: 115px; height: 75px; vertical-align: baseline; float: left">\n        <img src="http://img.avito.link/100x75/4603172004.jpg" alt="" style="max-width: 100px; max-height: 75px" />\n    </div>\n    <div style="vertical-align: baseline">\n      <h4 class="media-heading">iPhone 6 128 GB обмен</h4>\n      <p>\n        <span class="text-muted">Ставропольский край, Ставрополь, р-н Ленинский</span>\n        <br /><span class="text-muted">15 июля 2018\n      </p>\n    </div>\n  </div>\n  </a>\n\n  </div>\n  <div class="col-sm-3 col-sm-offset-1" style="text-align: center; margin-bottom: 2em">\n      <p class="text-muted">Другие форматы этого номера:<p><pre style="border: 0; background: none; color: #777">  9996539080\n 999 6539080\n   999 653-90-80</pre>\n  </div>\n</div>\n\n\n\n\n    </div> <!-- /container -->\n\n\t\t\t<script type="text/javascript" >\n\t\t\t\t (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};\n\t\t\t\t m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})\n\t\t\t\t (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");\n\n\t\t\t\t ym(62778595, "init", {\n\t\t\t\t\t\t\tclickmap:true,\n\t\t\t\t\t\t\ttrackLinks:true,\n\t\t\t\t\t\t\taccurateTrackBounce:true\n\t\t\t\t });\n\t\t\t</script>\n\t\t\t<noscript><div><img src="https://mc.yandex.ru/watch/62778595" style="position:absolute; left:-9999px;" alt="" /></div></noscript>\n\n  </body>\n</html>\n'
    ba_info = parse_by_bullshit_agency(pretty_info)
    pretty_info = helpers.escape_markdown(
        '📞bullshit.agency - Avito Запрос\n', version=2)+ba_info
    info = {"parse_mode": "MarkdownV2", "info": pretty_info}
    return info


def get_info_by_soup_query(query, social_type, Config, vk_session):
    fname = ""
    params = query.split(",")
    s_query = ''
    city = None
    age_from = None
    age_to = None
    for param in params:
        if param.find("q=") >= 0:
            s_query = param.replace("q=", "").strip()
        if param.find("city=") >= 0:
            city = param.replace("city=", "").strip()
        if param.find("a=") >= 0:
            tmp_age = param.replace("a=", "").strip()
            tmp_age = tmp_age.split("-")
            if(len(tmp_age) >= 2):
                age_from = tmp_age[0]
                age_to = tmp_age[1]
            else:
                age_from = age_to = tmp_age[0]
    # search_res = ok_api.user_search("", s_query, in_city=city, in_age_from=age_from, in_age_to=age_to)
    search_res = []
    if social_type == "ok":
        res = ok_api.auth(Config["ok_user_name"], Config["ok_password"])
        search_res = ok_api.user_search(
            res["session_key"], s_query, in_city=city, in_age_from=age_from, in_age_to=age_to)
    if social_type == "vk":
        search_res = vk_api_helper.user_search(
            vk_session, s_query, in_city=city, in_age_from=age_from, in_age_to=age_to)
    if search_res is None:
        return ""
    fname = generate_html_from_soup_profiles(search_res, social_type)
    return fname


def get_info_by_history(reque, connection, check_only=False):
    markdownv2_info = "not found"
    query = "select * from telebot_log_responses where message like '__%%" + \
        str(reque)+"%%'"
    if check_only:
        query = "select id from telebot_log_responses where message like '__%%" + \
            str(reque)+"%%'"
    result = postgres_helper.db_select_many(connection, query)
    if len(result) > 0:
        markdownv2_info = ''
    if not check_only:
        for req in result:
            markdownv2_info += "%s [%s] (%s) %s\n\n" % (str(req[6]),
                                                        req[3], req[4], req[5])
    info = {"parse_mode": "MarkdownV2",
            "info": markdownv2_info, "len": len(result)}
    info["info"] = helpers.escape_markdown(info["info"], version=2)
    return info
