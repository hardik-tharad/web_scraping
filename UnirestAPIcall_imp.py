
"""Web Scraping of Jabong page"""
#to make API calls
import unirest

#To parse html tag
from bs4 import BeautifulSoup

#To detect socket error
from socket import error as SocketError
import errno


from pprint import pprint
#To calculate time taken by the code to run
import time

#used to store data
import pandas as pd

#convert unicode to ascii
import unicodedata
import socket

start_time = time.time()


#database where everything is stored
database = {}
database['prod_url'] = []
database['prod_name'] = []
database['original_price'] = []
database['discounted_price'] = []

soup = None
#Function to parse the html data stored in soup
def parseData(soup):
	#find all required tags and store texts
	mydivs = soup.findAll("div", { "class" : "col-xxs-6 col-xs-4 col-sm-4 col-md-3 col-lg-3 product-tile img-responsive"})
	for tag in mydivs:
		if tag.find("a",{"href": True,"data-pos": True}):
			href_tag = tag.find("a",{"href": True,"data-pos": True})
			product_url =href_tag['href']
			#pprint(product_url)
			database['prod_url'].append(product_url)
			prod_name_tag =href_tag.find("div",{"class": "h4"})
			product_name = prod_name_tag.span.contents[0]
			product_name = unicodedata.normalize('NFKD', product_name).encode('ascii','ignore')
			#pprint(product_name)
			database['prod_name'].append(product_name)
			price_tag=prod_name_tag.next_sibling
			if(price_tag.span['class']==['prev-price']):
				org_price=price_tag.span.span.contents[0]
				dis_price= price_tag.span.next_sibling.contents[0]
			else:
				org_price=price_tag.span.contents[0]
				dis_price=org_price

			org_price=unicodedata.normalize('NFKD', org_price).encode('ascii','ignore')
			dis_price=unicodedata.normalize('NFKD', dis_price).encode('ascii','ignore')
			database['original_price'].append(org_price)
			database['discounted_price'].append(dis_price)
			#pprint(dis_price)
			#pprint(org_price)

#Function to make API calls and get data
 		
def getData(i):
	#To get rid of Socket Error
	try:
		response = unirest.get("http://www.jabong.com/men/clothing/polos-tshirts/", headers={ "Accept": "application/json" }, params = {"ax" : 1, "limit" : 52,"page" : i,"qc" : "men tshirt","rank": 0,"sortBy": "desc","sortField": "popularity","tt": "men ts"})
		global soup
		soup = BeautifulSoup(response.body,"lxml")
		time.sleep(.5)
		#pprint(soup)

	except SocketError as e:
	        if e.errno != errno.ECONNRESET:
	        	raise 
	    	pass 
	parseData(soup)

i=0
while i<=195: #since each page contains 52 products,so 195*52>10000
	getData(i)
	#print(i)
	i+=1

#convert dictionary to panda-dataframe
dataframe = pd.DataFrame(database,columns=['prod_url','prod_name','original_price','discounted_price'])

#convert panda-datafram to csv file
dataframe.to_csv('output.csv')

print
print
print

#Total time taken
print("Total time taken ")
pprint(time.time()-start_time)


