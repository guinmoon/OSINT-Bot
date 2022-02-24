import requests

def facebook_by_phone(phone):
    url = "https://api.eyecon-app.com/app/getoptionalpics.jsp?clipics=%s&cv=vc_332_vn_2.0.332_a"%phone
    payload = {}
    headers = {
    'accept': '*/*',
    'e-auth-v': 'e1',
    # 'e-auth': '49ae2519-2151-4a67-85bd-4e15afd00559',
    # 'e-auth-c': '22',
    'e-auth': '8025b1a7-51c6-48b7-be0e-c06778834f07',
    'e-auth-c': '40', 
    'accept-charset': 'UTF-8',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G955N Build/N2G48H)',
    'Host': 'api.eyecon-app.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.text.encode('utf8')
