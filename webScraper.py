
from bs4 import BeautifulSoup
from urllib.request import urlopen

#import re for part 2
import re

import mechanicalsoup
import time
    
#add url we want to scrapping
url = "https://www.ceb.lk/"
page = urlopen(url)
html = page.read().decode("utf-8")

     #part 1 get title on given web site
pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title) # Remove HTML tags
print(title)

    #part 2 get all data in text format in web site
soup = BeautifulSoup(html, "html.parser")
print(soup.get_text()) 

#find all images details in web site
soup.find_all("img")
image1= soup.find_all("img")
print(image1)

browser = mechanicalsoup.Browser()
page = browser.get(url)

#The number 200 represents the status code returned by the request. A status code of 200 means that the request was successful
#unsuccessful request might show a status code of 404 if the URL doesn’t exist or 500 if there’s a server error when making the request.

print(page)

#echanicalSoup uses Beautiful Soup to parse the HTML from the request, and page has a .soup attribute that represents a BeautifulSoup object

print(type(page.soup))
print(page.soup)

print(soup.get_text())

