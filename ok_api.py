import requests
import json
import urllib.parse
from  classes.soup_profile import *

def auth(login,password):
    url = "https://api.ok.ru/api/batch/executeV2"
    payload = 'application_key=CBAFJIICABABABABA&auth.login=&methods=%5B%0A%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%22auth.login%22%3A%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%22params%22%3A%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22client%22%3A%20%22android_8_20.4.20%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22deviceId%22%3A%20%22INSTALL_ID%3D030b17c2-f51d-4641-b860-c9230a751ec5%3BANDROID_ID%3D84949fde69b77119%3B%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22gen_token%22%3A%20true%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22password%22%3A%20%22'+password+'%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22user_name%22%3A%20%22'+login+'%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22verification_supported%22%3A%20true%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22verification_supported_v%22%3A%20%223%22%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%5D'
    headers = {
    'User-Agent': 'OKAndroid/20.4.20 b614 (Android 7.0; en_US; Android Custom Phone Build/vbox86p-userdebug 7.0 NRD90M 391 test-keys; xhdpi 320dpi 720x1184)',
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'bci=-3218965118927310717; _statid=b877bcdf-b9bd-40d6-9715-53452ec7df84'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    res = json.loads(response.text,encoding='utf8')[0]["ok"]
    return res

def user_search(session_key,search_string,in_city=None,in_age_from=None,in_age_to=None):
    url = "https://api.ok.ru/api/batch/executeV2"
    city = ''
    age_from = ''
    age_to = ''
    if in_city is not None:
        city = ',\\"city\\":\\"'+in_city+'\\"'
    if in_age_from is not None:
        age_from=',\\"min_age\\":'+str(in_age_from)
    if in_age_to is not None:
        age_to=',\\"max_age\\":'+str(in_age_to)     
    method = '[{"search.globalGrouped":{"params":{"count":100,"fieldset":"android.1","filters":"[{\\"type\\":\\"user\\"'+city+age_from+age_to+'}]","query":"'+search_string+'","screen":"GLOBAL_SEARCH_USERS_NO_RESULTS","types":"USER"}}}]'
    method = urllib.parse.quote_plus(method)
    payload = '389%0A__screen=feed_main&application_key=CBAFJIICABABABABA&methods='+method+'&session_key='+session_key            
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'OKAndroid/20.5.15 b619 (Android 7.1.2; en_US; samsung SM-G955N Build/N2G48H.G9550ZHU1AQEE; hdpi 240dpi 720x1280)',
    'Accept': 'application/json',    
    'Host': 'api.ok.ru',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Cookie': 'bci=-3218965118927310717; _statid=b877bcdf-b9bd-40d6-9715-53452ec7df84'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    if response.status_code!=200:
        return None
    res = json.loads(response.text,encoding='utf8')[0]["ok"]
    if "entities" not in res:
        return None
    res = res["entities"]["users"]
    method = '[{"users.getInfo":{"params":{"fields":"URL_PROFILE,name,last_name,first_name,pic190x190,last_online_ms,birthday,gender,age,location","uids":"'
    profile_num = 0
    profile_max = len(res)
    for profile in res:        
        method+=profile["uid"]
        if profile_num<profile_max-1:
            method+=","        
        profile_num+=1
    method+='"}}}]'
    method = urllib.parse.quote_plus(method)
    payload = '389%0A__screen=feed_main&application_key=CBAFJIICABABABABA&methods='+method+'&session_key='+session_key
    response = requests.request("POST", url, headers=headers, data = payload)
    if response.status_code!=200:
        return None
    response_text = response.text
    # response_text='[{"ok": {"user": {"uid": "296225027453", "birthday": "1981-08-13", "birthdaySet": true, "age": 39, "first_name": "виталий", "last_name": "принцев", "name": "виталий принцев", "gender": "male", "location": {"city": "армянск", "country": "UKRAINE", "countryCode": "UA", "countryName": "Украина"}, "pic190x190": "https://api.ok.ru/img/stub/user/male/190.png", "url_profile": "https://ok.ru/profile/520647022216"}}}, {"ok": {"user": {"uid": "781313734737", "birthday": "1964-03-08", "birthdaySet": true, "age": 56, "first_name": "Виталий", "last_name": "Принцев", "name": "Виталий Принцев", "gender": "male", "location": {"city": "", "country": "LITHUANIA", "countryCode": "LT", "countryName": "Литва"}, "last_online_ms": 1596024928396, "pic190x190": "https://i.mycdn.me/image?id=896535025572&t=33&plc=API&aid=25662464&tkn=*7IxTAQcbwLTnEukrGKQUBsDsbKA", "pic_base": "https://i.mycdn.me/image?id=896535025572&plc=API&aid=25662464&tkn=*9ZBEb26SwsxsndSb51gppJoSjKY", "url_profile": "https://ok.ru/profile/584811109284"}}}, {"ok": {"user": {"uid": "790953514277", "birthday": "1964-03-08", "birthdaySet": true, "age": 56, "first_name": "Виталий", "last_name": "Принцев", "name": "Виталий Принцев", "gender": "male", "location": {"city": "", "country": "KAZAKHSTAN", "countryCode": "KZ", "countryName": "Казахстан"}, "last_online_ms": 1562841392875, "pic190x190": "https://i.mycdn.me/image?id=868017411536&t=33&plc=API&aid=25662464&tkn=*Dw7OtCv_ymoknRxn5gs-_DDsF1Q", "pic_base": "https://i.mycdn.me/image?id=868017411536&plc=API&aid=25662464&tkn=*i61hMiEdGoaiGQsZJOCzic6JJIA", "url_profile": "https://ok.ru/profile/575124600528"}}}, {"ok": {"user": {"uid": "489604452981", "birthday": "1960-09-04", "birthdaySet": true, "age": 60, "first_name": "Виталий", "last_name": "Принцев", "name": "Виталий Принцев", "gender": "male", "location": {"city": "Нея", "country": "RUSSIAN_FEDERATION", "countryCode": "RU", "countryName": "Россия"}, "pic190x190": "https://api.ok.ru/img/stub/user/male/190.png", "url_profile": "https://ok.ru/profile/327460532608"}}}, {"ok": {"user": {"uid": "790581113250", "birthday": "1976-06-06", "birthdaySet": true, "age": 44, "first_name": "Виталий", "last_name": "Принцев", "name": "Виталий Принцев", "gender": "male", "location": {"city": "", "country": "RUSSIAN_FEDERATION", "countryCode": "RU", "countryName": "Россия"}, "last_online_ms": 1593185912654, "pic190x190": "https://i.mycdn.me/image?id=893997786711&t=33&plc=API&ts=0000000000000002e9&aid=25662464&tkn=*dChYBdYo-2P_1YjmshAaTqpkJFY", "pic_base": "https://i.mycdn.me/image?id=893997786711&ts=0000000000000002e9&plc=API&aid=25662464&tkn=*2pFbIUpTLeUBJcttPAqpwYsggUQ", "url_profile": "https://ok.ru/profile/574767911511"}}}, {"ok": {"user": {"uid": "484251374420", "birthday": "1960-09-04", "birthdaySet": true, "age": 60, "first_name": "Виталий", "last_name": "Принцев", "name": "Виталий Принцев", "gender": "male", "location": {"city": "Нея", "country": "RUSSIAN_FEDERATION", "countryCode": "RU", "countryName": "Россия"}, "last_online_ms": 1354118904770, "pic190x190": "https://i.mycdn.me/image?id=244905868961&t=33&plc=API&aid=25662464&tkn=*lVTxatpFh2mex4MDNgj2uOqtDa0", "pic_base": "https://i.mycdn.me/image?id=244905868961&plc=API&aid=25662464&tkn=*fWxYshPJkbmzVbqgn74EGaCpmng", "url_profile": "https://ok.ru/profile/332846968993"}}}, {"ok": {"user": {"uid": "779339494608", "birthday": "1964-03-08", "birthdaySet": true, "age": 56, "first_name": "Виталий", "last_name": "Принцев", "name": "Виталий Принцев", "gender": "male", "location": {"city": "", "country": "KAZAKHSTAN", "countryCode": "KZ", "countryName": "Казахстан"}, "last_online_ms": 1519628024691, "pic190x190": "https://i.mycdn.me/image?id=838633079077&t=33&plc=API&aid=25662464&tkn=*6UF8GHyCegbYbCVLL1AiG_5kVnU", "pic_base": "https://i.mycdn.me/image?id=838633079077&plc=API&aid=25662464&tkn=*iK4w2HrcncYZHpEDAWi1L_evTMc", "url_profile": "https://ok.ru/profile/587149661989"}}}]'
    profiles_ok = json.loads(response_text,encoding='utf8')[0]["ok"]
    profiles_soup = []
    for profile_ok in profiles_ok:
        descriptions = []
        profile_pic = ""
        if "pic190x190" in profile_ok:
            profile_pic = profile_ok["pic190x190"]
        if "age" in profile_ok:
            descriptions.append({"age":profile_ok["age"]})
        if "birthday" in profile_ok:
            descriptions.append({"birthday":profile_ok["birthday"]})
        if "location" in profile_ok:
            location = profile_ok["location"]
            if "city" in location:
                descriptions.append({"city":location["city"]})
            if "country" in location:
                descriptions.append({"countrys":location["country"]})
        tmp_soup_profile = SOUP_Profile(full_name=profile_ok["name"],profile_url=profile_ok["url_profile"],profile_pic=profile_pic,profile_descriptions=descriptions)
        profiles_soup.append(tmp_soup_profile)
    return profiles_soup