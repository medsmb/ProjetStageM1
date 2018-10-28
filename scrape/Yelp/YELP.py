#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from lxml import html  
import unicodecsv as csv
import requests
from exceptions import ValueError
from time import sleep
import re
import argparse
from unidecode import unidecode
import time

api_keys = ["AIzaSyBhB90fYYhqdbx0DPIUVxxJo9eDyLmBAQw","AIzaSyAMheeadgxknfBopskL_OcGDhBtAjQNHKI"]
myfile = open('New_Aquitaine_places_BD_LR.csv','w')
Doc=csv.writer(myfile)
# Doc.writerow( ['city','rank','business_name','review_count','global categorie','categories','rating','price_range','address','latitude','longitude','reservation_available','accept_pickup','url'])
#places = ["Bars","Restaurants","Food","Delivery","Takeout","Reservations"]
# cities=[]
cities=["Pau,64000"]
DEP=[]
COMM=[]
"""with open('New_aquitaine_cities.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader) # supression des entêtes
            for row in csv_reader:
                DEP.append(row[0]+"000") #l'ajout des département à la liste convenable
                COMM.append(row[1])
                cities.append(row[2]+" "+row[0]+row[1])"""
places = ["Coffee & Tea","Breakfast & Brunch","Bars","nightlife","Restaurants","Food","Delivery","Takeout","Reservations","home services"]
# cities=["la rochelle 17000","Bordeaux 33000"]
# places = ["Bars"]
for city in cities:
	myfile = open('%s.xls'%(city),'w')
	Doc=csv.writer(myfile)
	Doc.writerow( ['city','rank','business_name','review_count','categories','rating','price_range','address','latitude','longitude','reservation_available','accept_pickup','url'])
	
	k=0
	for place in places:
		id=0
		yelp_url  = "https://www.yelp.com/search?find_desc=%s&find_loc=%s&start=%s"%(place,city,str(id))
		headers1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
		response1 = requests.get(yelp_url).text
		parser = html.fromstring(response1)
		print "Parsing the page"
		listing1 = parser.xpath("//li[@class='regular-search-result']")
		total_results = parser.xpath("//span[@class='pagination-results-window']//text()")
			#print total_results
		for rr in total_results:
				test=rr.split("of")[1]
				print test
				nbpage=int(test)/30
				print nbpage
		scraped_datas=[]
		for i in range(0,int(nbpage)+1):
			scraped_datas.append("https://www.yelp.com/search?find_desc=%s&find_loc=%s&start=%s"%(place,city,str(id)))
			 
			id+=30
		
		for scrap in scraped_datas:
			print scrap
			#headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
			response = requests.get(scrap).text
			parser = html.fromstring(response)
			print "Parsing the page"
			listing = parser.xpath("//li[@class='regular-search-result']")
			for results in listing:
					raw_position = results.xpath(".//span[@class='indexed-biz-name']/text()")	
					raw_name = results.xpath(".//span[@class='indexed-biz-name']/a//text()")
					raw_name=raw_name
					raw_ratings = results.xpath(".//div[contains(@class,'rating-large')]//@title")
					raw_review_count = results.xpath(".//span[contains(@class,'review-count')]//text()")
					raw_price_range = results.xpath(".//span[contains(@class,'price-range')]//text()")
					category_list = results.xpath(".//span[contains(@class,'category-str-list')]//a//text()")
					raw_address = results.xpath(".//address//text()")
					print raw_address
					
					is_reservation_available = results.xpath(".//span[contains(@class,'reservation')]")
					is_accept_pickup = results.xpath(".//span[contains(@class,'order')]")
					url = "https://www.yelp.com"+results.xpath(".//span[@class='indexed-biz-name']/a/@href")[0]

					name = ''.join(raw_name).strip()
					name = unidecode(name)
					print unidecode(name)
					position = ''.join(raw_position).replace('.','')
					cleaned_reviews = ''.join(raw_review_count).strip()
					reviews =  re.sub("\D+","",cleaned_reviews)
					categories = ','.join(category_list) 
					cleaned_ratings = ''.join(raw_ratings).strip()
					for api_key in api_keys:
					
						api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(raw_address, api_key))
						api_response_dict = api_response.json()
						if api_response_dict['status'] == 'OK':
							latitude = api_response_dict['results'][0]['geometry']['location']['lat']
							longitude = api_response_dict['results'][0]['geometry']['location']['lng']
							print 'Latitude:', latitude
							print 'Longitude:', longitude
					if raw_ratings:
						ratings = re.findall("\d+[.,]?\d+",cleaned_ratings)[0]
					else:
						ratings = 0
					price_range = len(''.join(raw_price_range)) if raw_price_range else 0
					address  = ' '.join(' '.join(raw_address).split())
					address=unidecode(address)
					if city not in address:
							# address=address+" 17000 la Rochelle"
							address=address+" " + city
					reservation_available = True if is_reservation_available else False
					accept_pickup = True if is_accept_pickup else False
					data={
							'business_name':name,
							'rank':position,
							'review_count':reviews,
							'categories':categories,
							'rating':ratings,
							'price_range':price_range,
							'address':address,
							'latitude':latitude,
							'longitude':longitude,
							'reservation_available':reservation_available,
							'accept_pickup':accept_pickup,
							
							'url':url
					}
					#scraped_datas.append(data)
					Doc.writerow([city,position,name,reviews,place,categories,ratings,price_range,address,latitude,longitude,reservation_available,accept_pickup,url])
					time.sleep(10)
			# time.sleep(100)	
		# time.sleep(50)	
	time.sleep(10+k)	
	k+=2
time.sleep(30)					
