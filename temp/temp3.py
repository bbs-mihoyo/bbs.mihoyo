from bs4 import BeautifulSoup as BS

doc = BS(open('temp2.html', encoding='utf-8').read())

open('temp2.html', mode = 'w', encoding='utf-8').write(str(doc))