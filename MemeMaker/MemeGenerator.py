#All the things related to meme generation, might have to split this up
#If I'm going to be fucking networking I need a logger service too
import requests
from bs4 import BeautifulSoup

#don't parse html with REGEX! https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags

#Going to need a method to follow a pic.twitter URL, find the actual image source, and return it to the user
def picURLParser(URL):
    page = requests.get(URL) #placeholder, change to URL
    if(page.status_code != 200):
        print("requests are fucked")
    soup = BeautifulSoup(page.content, 'html.parser')
    #Test 1
    picData = soup.find(class_="AdaptiveMedia-photoContainer js-adaptive-photo")#ho boy I sure do hope this is standard
    picURL = picData.find()
    #Test 2
    #picData = soup.select("AdaptiveMedia-photoContainer js-adaptive-photo src")
    #realURL =
    return
#Going to need a method that takes in a top string, bottom string, and image source, and passes them off to the meme maker. Might save
#this image programatically, no clue how to do that

#Method to split text into top and bottom meme? I don't know if its even worth the effort, maybe just for fun


#Main test stuff, this should be on top come on python why you gotta enforce ordering
picURLParser("https://twitter.com/RT_com/status/942156129961877504/photo/1")
