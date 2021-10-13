# from gevent import monkey
# monkey.patch_all()
from bs4 import BeautifulSoup
import gevent,requests, bs4, selenium, gspread, csv, time
# from gevent.queue import Queue
from bs4 import BeautifulSoup
import requests
from bs4.dammit import EncodingDetector
from fpdf import FPDF 

rawstory=[]
titletext=''
def makelocalpdf():
    pdf = FPDF() 
    pdf.add_page() 
    pdf.set_font("Arial", size = 15) 
    f = rawstory
    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 
    pdf.output('/Users/ender/Dropbox/Python/Test/readsmart/Scrapy content/'+str(111)+'.pdf')
    #pdf.output('/Users/ender/Dropbox/Python/Test/readsmart/Scrapy content/'+str(titletext)+'.pdf')

material_url='http://www.qigushi.com/shuiqian/1024.html'

#http://www.qigushi.com/shuiqian/index_14.html
urllist=[]
material_url='http://www.qigushi.com/shuiqian/index_3.html'
def service():
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
            #titlefinal=titletext.partition('\n')[0]
            print(titletext)
            time.sleep(1)
        content=soup.find_all(class_='article_content')
        for z in content:
            rawstory=z.get_text()
            print(rawstory)
            #print(z.get_text())
        urllist.append(linklist)
        makelocalpdf()

for j in range(2,15):
    material_url='http://www.qigushi.com/shuiqian/index_'+str(j)+'.html'
    #print(j)
    service()
print(urllist)
