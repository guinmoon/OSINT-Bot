import vk_api
from  classes.soup_profile import *

def vk_search_same(vk_session,input_query):
    vk = vk_session.get_api()
    city = None
    age_from = None
    age_to = None
    if "city" in input_query:
        city = input_query["city"]
    if "age_from" in input_query:
        age_from = input_query["age_from"]
    if "age_to" in input_query:
        age_to = input_query["age_to"]
    res = vk.users.search(q=input_query["q"], count=input_query["count"],
                          fields=input_query["fields"], hometown=city, age_from=age_from, age_to=age_to)
    return res

def user_search(vk_session,search_string,in_city=None,in_age_from=None,in_age_to=None):
    vk = vk_session.get_api()
    city = None
    age_from = None
    age_to = None
    res = vk.users.search(q=search_string, count=100,
                          fields="photo,screen_name,photo_100,bdate,city,home_town,has_mobile", hometown=in_city, age_from=in_age_from, age_to=in_age_to)
    profiles_soup = []
    if len(res["items"])==0:
        return None
    for profile_vk in res["items"]:
        descriptions = []
        profile_pic = ""      
        full_name = profile_vk["first_name"]+" "+profile_vk["last_name"]
        profile_url = "https://vk.com/id"+str(profile_vk["id"])
        if "photo_100" in profile_vk:
            profile_pic = profile_vk["photo_100"]
        if "screen_name" in profile_vk:
            descriptions.append({"screen_name":profile_vk["screen_name"]})
        if "bdate" in profile_vk:
            descriptions.append({"bdate":profile_vk["bdate"]})
        if "city" in profile_vk:
            location = profile_vk["city"]
            if "title" in location:
                descriptions.append({"city":location["title"]})            
        tmp_soup_profile = SOUP_Profile(full_name=full_name,profile_url=profile_url,profile_pic=profile_pic,profile_descriptions=descriptions)
        profiles_soup.append(tmp_soup_profile)
    return profiles_soup