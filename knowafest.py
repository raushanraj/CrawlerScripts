import json
import requests
from lxml import html,etree
from html2text import html2text
from BeautifulSoup import BeautifulSoup as bs4
from multiprocessing.dummy import Pool as ThreadPool 
'''
python2.7 already installed on linux
sudo apt-get install pip
sudo pip install lxml
sudo pip install beautifulsoup
'''
def start_crawl(start_url,max_page):
	print "crawling started....."
	page=requests.get(start_url).text
	page=html.fromstring(page)
	links_on_page=page.xpath("//a[@class='btn-more hover-effect']/@href")
	pool = ThreadPool(5)
	results=pool.map(save_data_from_link,links_on_page)
	pool.close()
	pool.join()
	dump_to_json(results,max_page)
	next_page_link=page.xpath("//a[@id='Blog1_blog-pager-older-link']/@href")
	if next_page_link and max_page!=0:
		max_page=max_page-1
		start_crawl(next_page_link[0],max_page)
		
def save_data_from_link(link):
	final_data={}
	try:
		page=html.fromstring(requests.get(link).text)
		final_data['title']=page.xpath("//h3[@class='post-title entry-title']//div//p//text()")[0]
		all_dd=page.xpath("//dl[@class='dl-horizontal']//dd")
		all_dt=page.xpath("//dl[@class='dl-horizontal']//dt")
		for item in zip(all_dt,all_dd):
			final_data[bs4(etree.tostring(item[0])).text]=bs4(etree.tostring(item[1])).text
		final_data['about']=html2text(etree.tostring(page.xpath("//div[@id='info']")[0]))
		final_data['event']=html2text(etree.tostring(page.xpath("//div[@id='events']")[0]))
		final_data['register']=html2text(etree.tostring(page.xpath("//div[@id='register']")[0]))
		final_data['contact']=html2text(etree.tostring(page.xpath("//div[@id='contact']")[0]))
		final_data['tags']=page.xpath("//ul[@class='list-unstyled list-inline blog-tags']//a//text()")
		#about,event,register,contact are in Markdown-structured text
	except:
		pass
	return final_data

def dump_to_json(results,max_page):
	#Each json file will contains EVENT DETAILS of 5 events on listing page.
	json_file=open(str(max_page)+".json",'w+')
	json.dump(results,json_file)
	print "file "+str(max_page) +".json saved"
							
if __name__=="__main__":
	#set max page for the number of old posts you want to crawl 
	#each page contains 5 listings of event by default
	max_page=10
	#start_url is the home url or you can put any specific start url like Technical Events.default is for all
	start_url="http://www.knowafest.com/search?updated-max=2015-12-05T23:35:00%2B05:30&max-results=5"
	start_crawl(start_url,max_page)
	
	# output will be json,so any string refinement or conversion of markdown-text can be done in your preferred language
