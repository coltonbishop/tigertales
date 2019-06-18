import requests
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import time
import sys
import re
import csv,os,json
from lxml import html  
from time import sleep


#########################################################################################################
# THIS CODE SCRAPES BLACKBOARD AND CREATES THE JSON OBJECT FILE
#########################################################################################################


# Logs in by clicking the Guest Button of Blackboard 
# browser = webdriver.Chrome('/Users/Bishop/Desktop/TigerTales/chromedriver') #replace with .Firefox(), or with the browser of your choice
# url = "https://blackboard.princeton.edu/webapps/pu-readinglist-BB5932a686bf857/main.do?course_id=_6115714_1&mode=view"
# browser.get(url) #navigate to the page
# time.sleep(.5)
# submitButton = browser.find_element_by_xpath("//div[@class='btn'][3]") 
# submitButton.click() 
# browser.get(url) #navigate to the page
# a = 0

# data = json.load(open('data.json'))

newdata = []

# courseids = open('courseids.txt', 'r').readlines()
# i = -1
# x = 1
# y = 1
# length = len(courseids)
# print length
# progress = 1
# titles = []
# bookURLS = []

# for course in courseids:

# 	print str(progress) + " out of " + str(length) + " courses processed"
# 	progress = progress + 1

# 	i = i + 1


# 	url = "http://blackboard.princeton.edu/webapps/pu-readinglist-bb_bb60/find.jsp?courseid=" + course + "&term=1184"
# 	browser.get(url) #navigate to the page

# 	if i > 3:
# 		time.sleep(2)
# 	if i < 3:	
# 		time.sleep(3)

# 	try:
# 		courseTitle = browser.find_element_by_xpath("//li[@class='root coursePath']//a[@title]").text
# 		nextCourse = {"model": "app.Course", "pk": x, "fields": {"course_name": courseTitle,} }
# 		newdata.append(nextCourse)
# 		x = x + 1
# 	except:
# 		courseTitle = "No Title Found"
# 		nextCourse = {"model": "app.Course", "pk": x, "fields": {"course_name": courseTitle,} }
# 		newdata.append(nextCourse)
# 		x = x + 1
# 		e = sys.exc_info()[0]
# 		 # print e


#  	for w in range(1,15):

#  		# Adds photo url for the first book if it exists
#  		path = "//div[@class='viewReading'][" + str(w) + "]//div[@class='readingImage']//img['src']"
		
#  		try:
# 			imageurl = browser.find_element_by_xpath(path).get_attribute("src")
# 			bookURLS.append(imageurl)
# 			y = y + 1

# 		except:
#  			 e = sys.exc_info()[0]
#  			 # print e

# for url in bookURLS:
#  	print url

data = json.load(open('data.json'))
jsonURLS = json.load(open('urls.json'))



model = "app.Book"
pk = 0

coursenum = 0
i = 0
d = 0

print len(data["COURSE"])
for course in data["COURSE"]:
	puid = data["COURSE"][i]["COURSE_ID"][0]

	k = 0
	first = 0
	coursenum = coursenum + 1
	for book in data["COURSE"][i]["BOOK"]["LABYRINTH_PRICE"]:

		# if len(data["COURSE"][i]["BOOK"]["ASIN"]) == 0:
		# 	coursenum = coursenum + 1
		# 	continue

		# if first == 0:
		# 	coursenum = coursenum + 1
		# 	first = 1


		pk = pk + 1

		lab_price = data["COURSE"][i]["BOOK"]["LABYRINTH_PRICE"][k]
		try:
			amazon_price = data["COURSE"][i]["BOOK"]["AMAZON_PRICE"][k]
		except: 
			amazon_price = "No Price Available"

		if  not amazon_price: 
			amazon_price = "No Price Available"

		title = data["COURSE"][i]["BOOK"]["TITLE"][k]
		try:
			isbn_book = data["COURSE"][i]["BOOK"]["ISBN"][k]
		except:
			isbn_book = "ISBN Not Available"

		if d == len(jsonURLS[0]["website"]):
			continue

		courseID = i + 1
		nextBook = {
			"model": model,
			"pk": pk,
			"fields": {
				"title": title,
				"course": d,
				 "puid": puid,
				 "amazon_price": amazon_price,
				 "lab_price": lab_price,
				 "imageURL": jsonURLS[0]["website"][d],
				 "course_id": coursenum,
				 "isbn": isbn_book
			}
		}
		newdata.append(nextBook)
		k = k + 1
		d = d + 1


	k = 0
	i = i + 1



f=open('final.json','w')
json.dump(newdata,f,indent=4)





#########################################################################################################
#########################################################################################################






