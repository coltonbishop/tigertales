import requests
import time
import sys
import re
import csv,os,json

data = json.load(open('data.json'))

model = "app.Book"
pk = 0

books = []

print "here"
i = 0
for course in data["COURSE"]:

	puid = data["COURSE"][i]["COURSE_ID"][0]

	k = 0
	for book in data["COURSE"][i]["BOOK"]["LABYRINTH_PRICE"]:
		pk = pk + 1
		print data["COURSE"][i]["BOOK"]["TITLE"][k]
		print k
		lab_price = data["COURSE"][i]["BOOK"]["LABYRINTH_PRICE"][k]
		try:
			amazon_price = data["COURSE"][i]["BOOK"]["AMAZON_PRICE"][k]
		except: 
			amazon_price = "No Price Available"

		if  not amazon_price: 
			amazon_price = "No Price Available"

		title = data["COURSE"][i]["BOOK"]["TITLE"][k]
		nextBook = {
		    "model": model,
		    "pk": pk,
		    "fields": {
			    "title": title,
			    "course": 1,
			     # "puid": puid,
			     "amazon_price": amazon_price,
			     "lab_price": lab_price
		    }
	  	}
	 	books.append(nextBook)
	 	k = k + 1
	k = 0
	i = i + 1


print "here"
f=open('converted.json','w')
json.dump(books,f,indent=4)