from bs4 import BeautifulSoup as BS
from bs4.element import NavigableString
soup = BS(open('temp2.html', encoding='utf-8').read())
def change_link(item: BS):
    if isinstance(item, NavigableString): return
    if 'href' in item.attrs: 
        link = item['href']
        if link.startswith('/'): item['href'] = 'https://bbs.mihoyo.com' + link
    if 'src' in item.attrs: 
        link = item['src']
        if link.startswith('/'): item['src'] = 'https://bbs.mihoyo.com' + link
    for child in item.children: change_link(child)

change_link(soup)

open('temp2.html', mode='w', encoding='utf-8').write(str(soup))