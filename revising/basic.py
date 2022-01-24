from bs4 import BeautifulSoup as BS
from info import info
def set_stars(doc: BS, stars: int):
    lst = doc.find(class_ = 'obc-tmp-character__mobile--stars')
    lst2 = doc.find(class_ = 'obc-tmp-character__box--stars')
    lst.clear()
    lst2.clear()
    for i in range(stars): 
        lst.append(BS('<i class="obc-tmpl__rate-icon"></i>').i)
        lst2.append(BS('<i class="obc-tmpl__rate-icon"></i>').i)

def set_resume(doc: BS, info: dict):
    for item in doc.select('.obc-tmp-character__item'):
        key = item.find(class_ = 'obc-tmp-character__key').string
        item.find(class_ = 'obc-tmp-character__value').string = info[key.strip()]

def set_acsenion(doc: BS, materials: dict):
    upgrade_data = [
        [('ascension', 1, 1), ('plants', '', 3), ('monster', 1, 3)],
        [('ascension', 2, 3), ('boss', '', 2), ('plants', '', 10), ('monster', 1, 15)],
        [('ascension', 2, 6), ('boss', '', 4), ('plants', '', 20), ('monster', 2, 12)],
        [('ascension', 3, 3), ('boss', '', 8), ('plants', '', 30), ('monster', 2, 18)],
        [('ascension', 3, 6), ('boss', '', 12), ('plants', '', 45), ('monster', 3, 12)],
        [('ascension', 4, 6), ('boss', '', 20), ('plants', '', 60), ('monster', 3, 24)],
    ]
    item_list = doc.select('li.obc-tmpl__switch-item')
    for i in range(6):
        item = item_list[i+1]
        row_data = upgrade_data[i]
        lst = item.tbody.select('td')[1].ul
        lst.clear()
        for data in row_data:
            type, level, num = data
            name = materials[type]
            if isinstance(level, int):
                item_info = info[type][name][level-1]
            else:
                item_info = info[type][name]
            page_link = item_info["link"]
            item_name = item_info["name"]
            img_link = f"/img/{type}/{name}{level}.png"
            html = f'<li data-target="breach.attr.material" data-index="0"><div class="obc-tmpl__icon-text-num"><a target="_blank" href="{page_link}"><img src="{img_link}" alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">{item_name}</span></a> <span class="obc-tmpl__icon-num">*{num}</span></div></li>'
            lst.append(BS(html).li)

def set_learn_skill(doc: BS, skills: list, user_name: str):
    item_list = doc.select('li.obc-tmpl__switch-item')

    def set_one(i: int, name: str):
        item = item_list[i]
        grid = item.select('tbody')[1].tr.div
        grid.img["src"] = f"/img/talents/{user_name}{i}.png"
        grid.span.string = name
    
    set_one(1, skills[3]["name"])
    set_one(4, skills[4]["name"])

def set_stat(doc: BS, stat: list):
    item_list = doc.select('li.obc-tmpl__switch-item')
    for i in range(8):
        item = item_list[i]
        data = stat[i]
        rows = item.select('tbody')[1].select('tr')
        if i in (1, 4): rows = rows[1:]
        for j in range(len(rows)):
            grids = rows[j].select('td')
            grids[0].string = data[4*j]
            grids[1].span.string = data[4*j+1]
            grids[2].string = data[4*j+2]
            grids[3].span.string = data[4*j+3]
  
def set_recommend_weapon(doc: BS, equips: dict):
    table = doc.select(".obc-tmpl__part--recommend .obc-tmpl__switch-item tbody")[0]
    table.clear()
    equip_stat = info["weapon"]
    for key,value in equips.items():
        html = f'<tr><td><div class="obc-tmpl__icon-text-num"><a target="_blank" href="{equip_stat[key]}"><img src="/img/weapon/{key}.png" alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">{key}</span></a> <!----></div></td> <td class="obc-tmpl__recommend-reason"><p style="white-space: pre-wrap;">{value}</p></td></tr>'
        table.append(BS(html).tr)

def set_recommend_artifact(doc: BS, equips: dict, properties: list):
    table = doc.select(".obc-tmpl__part--recommend .obc-tmpl__switch-item tbody")[1]
    table.clear()
    equip_stat = info["artifact"]

    def p(content):
        return BS(f'<p style="white-space: pre-wrap; text-align: center;">{content}</p>').p
    for key,value in equips.items():
        content = BS('<td class="obc-tmpl__recommend-reason">').td
        content.append(p(value))
        content.append(p(f"<strong>时之沙：</strong>{properties[0]}"))
        content.append(p(f"<strong>空之杯：</strong>{properties[1]}"))
        content.append(p(f"<strong>理之冠：</strong>{properties[2]}"))
        content.append(p(f"<strong>副词条：</strong>{properties[3]}"))

        tr = BS('<tr></tr>').tr

        html = f'<td><div class="obc-tmpl__icon-text-num"><a target="_blank" href="{equip_stat[key]}"><img src="/img/artifact/{key}.png" alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">{key}</span></a> <!----></div></td>'
        left = BS(html).td
        right = content

        tr.append(left)
        tr.append(right)

        table.append(tr)

def set_map(doc: BS, profile: dict):
    id = info["plants"][profile["materials"]["plants"]]["map_id"]
    doc.find('iframe')["src"] = f"https://webstatic.mihoyo.com/app/ys-map-cn/index.html#/map/2?zoom=-2&center=153,-40&default_shown={id}&hidden-ui=true"

def revise_basic(doc: BS, profile: dict):
    set_resume(doc, profile["base_infos"])
    set_stars(doc, profile["star"])
    set_acsenion(doc, profile["materials"])
    set_learn_skill(doc, profile["skills"], profile["name"])
    set_stat(doc, profile["stat"])
    set_recommend_weapon(doc, profile["advised_equip"]["weapon"])
    set_recommend_artifact(doc, profile["advised_equip"]["artifact"], profile["advised_equip"]["artifact-properties"])
    set_map(doc, profile)