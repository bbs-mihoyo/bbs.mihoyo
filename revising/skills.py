from bs4 import BeautifulSoup as BS
from info import info

def revise_btn():
    pass

def upgrading_row(user_info, t):
    user_info['crown'] = '皇冠'
    upgrade_data = [
        [],
        [('books', 1, 3), ('monster', 1, 6)],
        [('books', 2, 2), ('monster', 2, 3)],
        [('books', 2, 4), ('monster', 2, 4)],
        [('books', 2, 6), ('monster', 2, 6)],
        [('books', 2, 9), ('monster', 2, 9)],
        [('books', 3, 4), ('monster', 3, 4), ('treasures', '', 1)],
        [('books', 3, 6), ('monster', 3, 6), ('treasures', '', 1)],
        [('books', 3, 12), ('monster', 3, 9), ('treasures', '', 2)],
        [('books', 3, 16), ('monster', 3, 12), ('treasures', '', 2), ('crown', '', 1)],
    ]
    res = BS('<tr><td>升级材料</td></tr>').tr
    for lvl in upgrade_data:
        grid = BS('<td></td>').td
        for item in lvl:
            type, level, num = item
            name = user_info[type]
            if isinstance(level, int):
                item_info = info[type][name][level-1]
            else:
                item_info = info[type][name]
            page_link = item_info["link"]
            item_name = item_info["name"]
            img_link = f"/img/{type}/{name}{level}.png"
            html = f'<div><div class="obc-tmpl__icon-text-num"><a target="_blank" href="{page_link}"><img src="{img_link}" alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">{item_name}</span></a> <span class="obc-tmpl__icon-num">*{num}</span></div></div>'
            grid.append(BS(html).div)
        res.append(grid)
    
    if t == "普攻": res.append(BS('<td>达达利亚天赋解锁（达达利亚在队伍时）</td>').td)
    elif t in ["元素战技", "元素爆发"]: 
        for i in range(3): res.append(BS('<td>命之座解锁</td>').td)
    return res
    #'<td><div><div class="obc-tmpl__icon-text-num"><a target="_blank" href="/ys/obc/content/830/detail"><img src="https://uploadstatic.mihoyo.com/ys-obc/2020/09/18/75795471/8653105260b2d2e039ef7e2e154f6d6b_4890924820178776981.png" alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">「繁荣」的教导</span></a> <span class="obc-tmpl__icon-num">*3</span></div></div><div><div class="obc-tmpl__icon-text-num"><a target="_blank" href="/ys/obc/content/1065/detail"><img src="https://uploadstatic.mihoyo.com/ys-obc/2020/09/18/75795471/d4ecf37daea86f2ef234c1f1155be97d_7379723812755521701.png" alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">骗骗花蜜</span></a> <span class="obc-tmpl__icon-num">*6</span></div></div></td>'

def revise_table(table: BS, skill_data, user_data, type):
    table.clear()

    for row_data in skill_data: 
        content = "".join([f"<td>{s}</td>" for s in row_data])
        table.append(BS(f"<tr>{content}</tr>").tr)
    
    table.append(upgrading_row(user_data, type))
    


def revise_skill(doc, profile):
    talents = doc.select('.ling-talent .obc-tmpl__switch-list li')
    #talents.clear()
    data = profile['skills']
    #「」
    for i in range(6):
        item = talents[i]
        info = data[i]
        item.find(class_ = 'obc-tmpl__icon-text').string = info["name"]
        item.find('pre', class_ = "obc-tmpl__pre-text").string = info["description"]
        item.h3.img["src"] = f"/img/talents/{profile['name']}{i}.png"
        item["height"] = info["height"]
        if not info["upgradable"]: continue
        revise_table(item.select('.obc-tmpl__scroll-x-box tbody')[0], info["data"], profile["materials"], info["type"])

def revise_stellation(doc: BS, profile: dict):
    charc_name = profile["name"]
    info_table = profile['constellation']
    rows = doc.select('.obc-tmpl__part--life tbody tr')
    for i in range(6):
        row = rows[i]
        info_row = info_table[i]
        name, material, description = row.select('td')

        name.img["src"] = f"/img/constellation/{charc_name}{i}.png"
        name.span.string = info_row[0]

        material.find(class_ = "obc-tmpl__icon-text").string = f"{charc_name}的命座"

        description.string = info_row[1]

def revise_talent(doc, profile):
    revise_skill(doc, profile)
    revise_stellation(doc, profile)

