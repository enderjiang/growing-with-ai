from bs4 import BeautifulSoup
import requests,os
from bs4.dammit import EncodingDetector
# set root folder as base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
urllist=[]
material_url='http://www.qigushi.com/shuiqian/index_3.html'
def service():
    global fulltitle
    titletext=''
    rawstory=''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
    source=requests.get(material_url)
    soup=BeautifulSoup(source.text,'html.parser')
    #print(soup)
    content=soup.find_all(class_='story_header')
    for z in content:
        linklist=z.find('a')['href']
        print(linklist)
        source=requests.get(linklist)
        http_encoding = source.encoding if 'charset' in source.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(source.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(source.content, 'lxml', from_encoding=encoding)
        #title=soup.find_all(class_=['post','title'])
        title=soup.find_all(class_='breadcrumb')
        for m in title:
            titletext=m.get_text()
            print('continue....')
            #titlefinal=titletext.partition('\n')[0]
            #time.sleep(1)
        content=soup.find_all(class_='article_content')
        for z in content:
            rawstory=z.get_text()
        urllist.append(linklist)
        print(titletext)
        print(rawstory)

for j in range(2,15):
    material_url='http://www.qigushi.com/shuiqian/index_'+str(j)+'.html'
    #print(j)
    service()