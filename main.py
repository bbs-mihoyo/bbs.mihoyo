from statistics import mode
from bs4 import BeautifulSoup as BS
from revising.skills import revise_talent
from revising.others import trim, revise_name
from revising.basic import revise_basic
import json

doc = BS(open('temp.html', encoding='utf-8').read())
profile = json.load(open('profile\\蒙古上单.json', encoding='utf-8'))

revise_basic(doc, profile)
revise_talent(doc, profile)
revise_name(doc, profile["name"])

trim(doc)

open('蒙古上单.html', mode = 'w', encoding='utf-8').write(str(doc))