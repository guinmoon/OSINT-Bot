
import json
from telegram.utils import helpers
from lxml import html
import time

def parse_numbuster_local(nb_json):
    pretty_info = ''
    phone_info = json.loads(nb_json)
    pretty_info += phone_info["region"]
    for name in phone_info["names"]:
        pretty_info += "\n%s" % name
    return pretty_info


def parse_vk100m_info_cerebro(vk100m_str):
    pretty_info = vk100m_str
    info_pretty_parts = vk100m_str.split('||')
    if len(info_pretty_parts)==3:
        pretty_info = "Имя ВК: %s\nЛогин ВК: %s\nПароль ВК:%s"%(info_pretty_parts[0],info_pretty_parts[1],info_pretty_parts[2])
    return pretty_info

def parse_avito_info_cerebro(vk100m_str):
    pretty_info = vk100m_str
    info_pretty_parts = vk100m_str.split('||')   
    if len(info_pretty_parts)>0:
        pretty_info = "Имя: %s"%(info_pretty_parts[0])
    if len(info_pretty_parts)>1:
        pretty_info+="\n Обьявления:\n"
        for i in range (1,len(info_pretty_parts)):
            pretty_info+="%i) %s\n"%(i,info_pretty_parts[i])

    return pretty_info

def parse_getcontact(gc_json):
    pretty_info = ''
    pretty_info += gc_json["phoneNumber"]
    pretty_info += ' '+gc_json["displayName"]
    for tag in gc_json["tags"]:
        pretty_info += "\n%s" % tag
    return pretty_info

def parse_eyecon(info):
    url = "not found."
    f_ind = info.find("facebook.com")
    if f_ind > 0:
        p_ind = info.find("/picture")
        url = "https://"+info[f_ind:p_ind]
    return url

def parse_numbuster(nb_json):
    pretty_info = ''
    pretty_info += nb_json["phones"][0]
    pretty_info += ' '+nb_json["region"]
    pretty_info += "\n%s %s" % (nb_json["firstName"], nb_json["lastName"])
    for contact in nb_json["contacts"]:
        pretty_info += "\n%s %s (%i)" % (contact["firstName"],
                                         contact["lastName"], contact["count"])
    return pretty_info

def parse_ok_info(ok_json):
    pretty_info = 'not found'
    if ok_json != "false\n":
        user = json.loads(ok_json)["users"][0]
        age = ""
        birthday = ""
        if "birthday" in user:
            birthday = user["birthday"]+" д.р."
        if "age" in user:
            age = str(user["age"])+" лет"
        location = ""
        if "location" in user:
            if "city" in user["location"]:
                location = '\n%s'%user["location"]['city']
        title = "%s %s %s %s %s" % (user["first_name"], user["last_name"],birthday, age,location)
        title = helpers.escape_markdown(title, version=2)
        pretty_info = "%s\n[ссылка на профиль](%s)" % (title, user["url_profile"])
        # pretty_info += "\n[Photo](%s)" % (user["pic600x600"])
    return pretty_info

def parse_ok_info_cerebro(ok_str):
    pretty_info = ok_str
    ok_info = ok_str.split('||')
    if len(ok_info)==2:
        pretty_info = '%s\nhttps://ok.ru/profile/%s'%(ok_info[1],ok_info[0])
    return pretty_info

def parse_vk_info(vk_profiles):
    pretty_info = 'not found'
    if (vk_profiles["count"] <= 0):
        return {"parse_mode": "MarkdownV2", "info": pretty_info}
    pretty_info = 'Профили Вконтакте:'
    for item in vk_profiles["items"]:
        # pretty_info += "\n%s %s"%(item["first_name"],item["last_name"])
        item["first_name"] = helpers.escape_markdown(item["first_name"], version=2)
        item["last_name"] = helpers.escape_markdown(item["last_name"], version=2)
        pretty_info += "\n[%s %s](https://vk.com/id%s)" % (
            item["first_name"], item["last_name"], item["id"])
        pretty_info += "\nid%s" % (item["id"])
        pretty_info += "\n[Photo](%s)" % (item["photo_200"])
    return {"parse_mode": "MarkdownV2", "info": pretty_info, "json": vk_profiles}



def parse_by_bullshit_agency(data):
    pretty_info = "not found"
    tree = html.fromstring(data)
    links = tree.xpath('//div[@class="col-sm-8"]')
    if len(links)<1:
        return pretty_info
    links = links[0]
    a_elems = links.xpath('//a')    
    if len(a_elems)>0:
        pretty_info = ''
    for a_elem in a_elems:
        attrib = a_elem.attrib
        href = 'https://mirror.bullshit.agency'+attrib["href"]
        description = a_elem.text_content()
        description = description.replace('\n',' ')
        # description = description.replace('  ',' ')
        description = " ".join(description.split())
        description = helpers.escape_markdown(description, version=2)
        pretty_info+='[%s](%s)\n\n'%(description,href)
    return pretty_info


def generate_html_from_soup_profiles(soup_profiles,social_type):
    fname= ""
    html_header = '<html><head><meta charset="utf-8"></head><body><table>\n'
    html = html_header
    for profile in soup_profiles:
        html += '<tr><td><span>'+profile.full_name+'</span>'
        html += '<a href="'+profile.profile_url+'"><img src="'+profile.profile_pic+'">'
        html += "</td><td>"
        for description in profile.profile_descriptions:
            for key, value in description.items():
                html += "<span>"+key+":"+str(value)+"</span><br>"
        html += "</td><tr>\n"
    html +="</table></body></html>"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fname = "reports/%sreport%s.html" %(social_type, timestr)
    report_file = open(fname, "wt")
    n = report_file.write(html)
    report_file.close()
    return fname
