from bs4 import BeautifulSoup as BS
def delete_comment(doc: BS): 
    for item in doc.find_all(class_ = "mhy-comment"): item.extract()
def delete_footer(doc: BS): 
    for item in doc.find_all(class_ = "footer"): item.extract()

def trim(doc: BS):
    delete_comment(doc)
    delete_footer(doc)

def revise_name(doc: BS, name: str):
    doc.find('title').string = f"{name}-履刑者创作平台-观测枢-原神wiki"
    doc.find(class_ = 'detail__title').string = name 
    doc.find(class_ = 'obc-tmp-character__mobile--title').string = name
    doc.find(class_ = 'obc-tmp-character__box--title').string = name
    doc.select('nav.header h1')[0].string = name