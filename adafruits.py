#scraper for http://www.adafruit.com/
from BeautifulSoup import *
#from nextpage import *
import urllib
import MySQLdb
#library to take care of the unicode problem
#More info here : http://stackoverflow.com/a/1207479
import unicodedata

db=MySQLdb.connect("127.0.0.1","root","","adafruit_products" )
cursor=db.cursor()
cursor.execute("TRUNCATE TABLE `products`")


def scrap_to_insert_in_DB(url):
    dbIndex=[]
    list1=[]
    page=get_source(url)
    index=scrap(page)
    #print index
    #print "hmmm"
    for key in index:
        for url in index[key]:
           # print key,url
            j=findDetail(key,url,list1)
           # print j
            print "                                     next        ----------------------------------"
            for products in j:
                insertindb(products[0],products[1].replace("'","`"),products[2],products[3],products[4],products[5],products[6])
                

def insertindb(a,b,c,d,e,f,g):
    #db=MySQLdb.connect("127.0.0.1","root","19890101","adafruit_products" )
    #cursor=db.cursor()
    sql="insert into products(category,productname,price,idstatus,parenturl,productdetailurl,outgoingurl)VALUES('%s','%s','%s','%s','%s','%s','%s')"%(a,b,c,d,e,f,g)
    print sql
    cursor.execute(sql)

def scrap(page):
    soap=BeautifulSoup(page)
    AllLink=soap.findAll('a')
   # print AllLink
    index={}
    for link in AllLink:
        linkstr=str(link)
        if linkstr.find('class="category-top"')!=-1 or linkstr.find('class="category-products"')!=-1:
           # print linkstr
            linktext=str(link.text)
            linktext=remove_nbsp(linktext)
            linkvalue=findlink(linkstr)
            if linktext in index and linkvalue!="":
                index[linktext].append(linkvalue)
            else:
                if linkvalue!="":
                    index[linktext]=[linkvalue]

    return index
                    

def get_source(url):
    try:
        sock=urllib.urlopen(url)
        pagesource=sock.read()
        return pagesource
    except:
        return ""

    
def remove_nbsp(linktext):
    start_nb=linktext.find("&nbsp;")
    if start_nb==-1:
        return linktext
    else:
        return linktext[:start_nb]
                
def findlink(page):
    start_link=page.find('href=')
    if start_link==-1:
        return ""
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url




def findDetail(key,url,list1):
    page=get_source(url)
    listE=findEvenDetail(key,url,page,list1)
    listO=findOddDetail(key,url,page,list1)
    return union(listE,listO)


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
    return p


def findEvenDetail(key,url,page,list1):
    while True:
        start=page.find('<tr  class="productListing-even">')
        if start!=-1:
            end=page.find('</tr>',start+1)
            strn=page[start:end+5]
            soap=BeautifulSoup(strn)
            l=soap.findAll('td')
            try:
                model=str(l[1].find('a').text)
            except:
                model=unicodedata.normalize('NFKD',l[1].find('a').text).encode('ascii','ignore')
                #model="unicode error"
                print model
            try:
                price=str(l[2].text)
            except:
                price=unicodedata.normalize('NFKD',l[2].text).encode('ascii','ignore')
                #price="unicode error"
                print price
            try:
                p_id_start=str(l[1].text).find('ID :')
                p_id=str(l[1].text)[p_id_start:]
            except:
                p_id_start=unicodedata.normalize('NFKD',l[1].text).encode('ascii','ignore').find('ID :')
                p_id=unicodedata.normalize('NFKD',l[1].text).encode('ascii','ignore')[p_id_start:]
                #p_id="unicode error"
                print p_id
            try:
                c_url=findlink(str(l[1].find('a')))
                o_url=findlink(str(l[2].find('a')))
            except:
                c_url="not yet"
                o_url="not yet"
            list1.append([key,model,price,p_id,url,c_url,o_url])
            page=page[end+5:]
        else:
            break
    return list1
        
    
def findlink(page):
    start_link=page.find('href=')
    if start_link==-1:
        return ""
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url 
                       
def findOddDetail(key,url,page,list1):
    while True:
        start=page.find('<tr  class="productListing-odd">')
        if start!=-1:
            end=page.find('</tr>',start+1)
            strn=page[start:end+5]
            soap=BeautifulSoup(strn)
            l=soap.findAll('td')
            try:
                model=str(l[1].find('a').text)
            except:
                model=unicodedata.normalize('NFKD',l[1].find('a').text).encode('ascii','ignore')
                #model="unicode error"
                print model
            try:
                price=str(l[2].text)
            except:
                price=unicodedata.normalize('NFKD',l[2].text).encode('ascii','ignore')
                #price="unicode error"
                print price
            try:
                p_id_start=str(l[1].text).find('ID :')
                p_id=str(l[1].text)[p_id_start:]
            except:
                p_id_start=unicodedata.normalize('NFKD',l[1].text).encode('ascii','ignore').find('ID :')
                p_id=unicodedata.normalize('NFKD',l[1].text).encode('ascii','ignore')[p_id_start:]
                #p_id="unicode error"
                print p_id
            try:
                c_url=findlink(str(l[1].find('a')))
                o_url=findlink(str(l[2].find('a')))
            except:
                c_url="not yet"
                o_url="not yet"
            list1.append([key,model,price,p_id,url,c_url,o_url])
            page=page[end+5:]
        else:
            break
    return list1

def iterate_and_get():
    index=scrap(get_source("http://www.adafruit.com/"))
    list1=[]
    for key in index:
        l=findDetail(key,index[key][0],list1)
        #print l

url="http://www.adafruit.com/"
scrap_to_insert_in_DB(url)
