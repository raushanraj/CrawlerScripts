import requests
import json

headers = {'content-type': 'application/json'}
url = 'https://uj5wyc0l7x-dsn.algolia.io/1/indexes/Item_production/query'


#there are 40 pages 
def getAllFbPosts():
	all_data=[]
	for i in range(40):
		query="query=facebook&hitsPerPage=25&page="+str(i)+"&getRankingInfo=1&minWordSizefor1Typo=5&minWordSizefor2Typos=9&tagFilters=%5B%22story%22%5D&numericFilters=%5B%5D&advancedSyntax=true&queryType=prefixNone"
		params = {"params":query,"apiKey":"8ece23f8eb07cd25d40262a1764599b1","appID":"UJ5WYC0L7X"}
		response=requests.post(url,data=json.dumps(params),headers=headers)
		hits=json.loads(response.text)["hits"]
		for hit in hits:
			fbpost={}
			fbpost['title']=hit['title']
			fbpost['url']=hit['url']
			fbpost['author']=hit['author']
			fbpost['posted_date']=hit['created_at']
			fbpost['comments']=hit['num_comments']
			fbpost['total_points']=hit['points']
			all_data.append(fbpost)
	print "Saving to Json...."
	return all_data
		
print "Crawling Data....."
all_data=getAllFbPosts()

with open('output_data.json', 'w') as outfile:
    json.dump(all_data, outfile,sort_keys=True, indent=4, separators=(',', ': '))

print "File Saved Successfully Please check output_data.json"
	
