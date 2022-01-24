import json


from bs4 import BeautifulSoup as BS

doc = BS(open('keaya.html', encoding='utf-8').read())
for item in doc.select('li.obc-tmpl__switch-item'):
    body = item.select('tbody')[1]
    res = []
    for row in body.select('tr'):
        res += ["".join(grid.strings).strip() for grid in row.select('td')]
    print(json.dumps(res, ensure_ascii=False)+",")