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
# THIS CODE CONVERTS ISBN TO ASIN
#########################################################################################################

def isbn_strip(isbn):
	"""Strip whitespace, hyphens, etc. from an ISBN number and return
the result."""
	short=re.sub("\W","",isbn)
	return re.sub("\D","X",short)

def convert(isbn):
	"""Convert an ISBN-10 to ISBN-13 or vice-versa."""
	short=isbn_strip(isbn)
	if (isValid(short)==False):
		raise "Invalid ISBN"
	if len(short)==10:
		stem="978"+short[:-1]
		return stem+check(stem)
	else:
		if short[:3]=="978":
			stem=short[3:-1]
			return stem+check(stem)
		else:
			raise "ISBN not convertible"

def isValid(isbn):
	"""Check the validity of an ISBN. Works for either ISBN-10 or ISBN-13."""
	short=isbn_strip(isbn)
	if len(short)==10:
		return isI10(short)
	elif len(short)==13:
		return isI13(short)
	else:
		return False

def check(stem):
	"""Compute the check digit for the stem of an ISBN. Works with either
	the first 9 digits of an ISBN-10 or the first 12 digits of an ISBN-13."""
	short=isbn_strip(stem)
	if len(short)==9:
		return checkI10(short)
	elif len(short)==12:
		return checkI13(short)
	else:
		return False

def checkI10(stem):
	"""Computes the ISBN-10 check digit based on the first 9 digits of a
stripped ISBN-10 number."""
	chars=list(stem)
	sum=0
	digit=10
	for char in chars:
		sum+=digit*int(char)
		digit-=1
	check=11-(sum%11)
	if check==10:
		return "X"
	elif check==11:
		return "0"
	else:
		return str(check)

def isI10(isbn):
	"""Checks the validity of an ISBN-10 number."""
	short=isbn_strip(isbn)
	if (len(short)!=10):
		return False
	chars=list(short)
	sum=0
	digit=10
	for char in chars:
		if (char=='X' or char=='x'):
			char="10"
		sum+=digit*int(char)
		digit-=1
	remainder=sum%11
	if remainder==0:
		return True
	else:
		return False

def checkI13(stem):
	"""Compute the ISBN-13 check digit based on the first 12 digits of a
	stripped ISBN-13 number. """
	chars=list(stem)
	sum=0
	count=0
	for char in chars:
		if (count%2==0):
			sum+=int(char)
		else:
			sum+=3*int(char)
		count+=1
	check=10-(sum%10)
	if check==10:
		return "0"
	else:
		return str(check)

def isI13(isbn):
	"""Checks the validity of an ISBN-13 number."""
	short=isbn_strip(isbn)
	if (len(short)!=13):
		return False
	chars=list(short)
	sum=0
	count=0
	for char in chars:
		if (count%2==0):
			sum+=int(char)
		else:
			sum+=3*int(char)
		count+=1
	remainder=sum%10
	if remainder==0:
		return True
	else:
		return False

def toI10(isbn):
	"""Converts supplied ISBN (either ISBN-10 or ISBN-13) to a stripped
ISBN-10."""
	if (isValid(isbn)==False):
		raise "Invalid ISBN"
	if isI10(isbn):
		return isbn_strip(isbn)
	else:
		return convert(isbn)

def toI13(isbn):
	"""Converts supplied ISBN (either ISBN-10 or ISBN-13) to a stripped
ISBN-13."""
	if (isValid(isbn)==False):
		raise "Invalid ISBN"
	if isI13(isbn):
		return isbn_strip(isbn)
	else:
		return convert(isbn)

def url(type,isbn):
	"""Returns a URL for a book, corresponding to the "type" and the "isbn"
provided. This function is likely to go out-of-date quickly, and is
provided mainly as an example of a potential use-case for the module.
Currently allowed types are "google-books" (the default if the type is
not recognised), "amazon", "amazon-uk", "blackwells".
"""
	short=toI10(isbn)
	if type=="amazon":
		return "http://www.amazon.com/o/ASIN/"+short
	elif type=="amazon-uk":
		return "http://www.amazon.co.uk/o/ASIN/"+short
	elif type=="blackwells":
		return "http://bookshop.blackwell.co.uk/jsp/welcome.jsp?action=search&type=isbn&term="+short
	else:
		return "http://books.google.com/books?vid="+short

#########################################################################################################
#########################################################################################################

#########################################################################################################
# THIS CODE SCRAPES AMAZON 
#########################################################################################################

def AmzonParser(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	page = requests.get(url,headers=headers)
	xCount = 0
	while True:
		sleep(3)
		try:
			xCount = xCount + 1
			doc = html.fromstring(page.content)
			XPATH_NAME = '//h1[@id="title"]//text()'
			XPATH_SALE_PRICE = '//span[contains(@class, "a-size-medium a-color-price header-price") or contains(@class, "a-size-small a-color-price") or contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
 
 
			RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)

			SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
 
			if page.status_code!=200:
				raise ValueError('captha')
			data = {
					'SALE_PRICE':SALE_PRICE,
					}
 
			return data['SALE_PRICE']
		except Exception as e:
			print e
			if XCount == 10:
				return "No Price Found"
 
def ReadAsin(asin):
	# AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))

		url = "http://www.amazon.com/dp/"+asin
		return AmzonParser(url)

#########################################################################################################
#########################################################################################################



#########################################################################################################
# THIS CODE SCRAPES BLACKBOARD AND CREATES THE JSON OBJECT FILE
#########################################################################################################


# Creates the JSON object
courses = {

	'COURSE': []

	}

# Logs in by clicking the Guest Button of Blackboard 
browser = webdriver.Chrome('/Users/Bishop/Desktop/TigerTales/chromedriver') #replace with .Firefox(), or with the browser of your choice
url = "https://blackboard.princeton.edu/webapps/pu-readinglist-BB5932a686bf857/main.do?course_id=_6115714_1&mode=view"
browser.get(url) #navigate to the page
time.sleep(.5)
submitButton = browser.find_element_by_xpath("//div[@class='btn'][3]") 
submitButton.click() 
browser.get(url) #navigate to the page
a = 0


courseids = open('courseids.txt', 'r').readlines()
i = -1

length = len(courseids)
print length
progress = 1

for course in courseids:

	print str(progress) + " out of " + str(length) + " courses processed"
	progress = progress + 1

	i = i + 1

	newCourse = {'COURSE_ID': [], 'BOOK': {'TITLE': [], 'ISBN': [],'ASIN': [],'LABYRINTH_PRICE': [],'AMAZON_PRICE': [],}}

	courses['COURSE'].append(newCourse)

	courses['COURSE'][i]['COURSE_ID'].append(course.strip('\n'))

	url = "http://blackboard.princeton.edu/webapps/pu-readinglist-bb_bb60/find.jsp?courseid=" + course + "&term=1184"
	browser.get(url) #navigate to the page
	if i > 3:
		time.sleep(2)
	if i < 3:	
	time.sleep(3)


	# Prints the info for the first book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][1]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:
		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][1]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))
	except:
		a = 1

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][1]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1


	# Prints the info for the second book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][2]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][2]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))
	except:
		a = 1

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][2]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1



	# Prints the info for the third book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][3]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue


	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][3]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1


	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][3]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the fourth book if it exists
	try:
		 courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][4]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue


	try:
		isbn =  browser.find_element_by_xpath("//div[@class='viewReading'][4]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][4]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the fifth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][5]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue


	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][5]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			


	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][5]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1


	# Prints the info for the sixth book if it exists
	try:
		 courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][6]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn =  browser.find_element_by_xpath("//div[@class='viewReading'][6]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][6]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the seventh book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][7]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][7]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][7]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1


	# Prints the info for the eigth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][8]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][8]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][8]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1


	# Prints the info for the ninth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][9]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][9]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][9]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the tenth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][10]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][10]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][10]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the eleventh book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][11]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][11]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][11]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1


	# Prints the info for the twelfth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][12]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][12]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][12]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the thirteenth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][13]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][13]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][13]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1

	# Prints the info for the fourteenth book if it exists
	try:
		courses['COURSE'][i]['BOOK']['TITLE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][14]//tbody[1]/tr[2]/td[@class='textBold'][1][1][1]").text)
	except:

		continue

	try:
		isbn = browser.find_element_by_xpath("//div[@class='viewReading'][14]//tbody[1]/tr[4]/td[@class='textBold'][1][1][1]").text
		courses['COURSE'][i]['BOOK']['ISBN'].append(isbn)
		asin = convert(isbn)
		courses['COURSE'][i]['BOOK']['ASIN'].append(asin)
		courses['COURSE'][i]['BOOK']['AMAZON_PRICE'].append(ReadAsin(asin))

	except:
		a = 1			

	try:
		courses['COURSE'][i]['BOOK']['LABYRINTH_PRICE'].append(browser.find_element_by_xpath("//div[@class='viewReading'][14]//td[@class='shoppingCartInfo']/div[@class='textElementItalic' or 'textElement']").text)
	except:
		a = 1


f=open('data.json','w')
json.dump(courses,f,indent=4)


#########################################################################################################
#########################################################################################################

