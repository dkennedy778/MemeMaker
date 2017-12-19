#All the things related to meme generation, might have to split this up
#If I'm going to be fucking networking I need a logger service too
import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib

#don't parse html with REGEX! https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags
i = 0

#Going to need a method to follow a pic.twitter URL, find the actual image source, and return it to the user
def picURLParser(URL):
    page = requests.get(URL) #placeholder, change to URL
    if(page.status_code != 200):
        print("requests are fucked")
    soup = BeautifulSoup(page.content, 'html.parser')
    # ho boy I sure do hope twitter's image embedding is standardized
    picData = soup.find(id="permalink-overlay")
    link = picData.find('img')
    URL = link.attrs['src'] #getting the wrong picture, gotta think about this some more
    return URL

#Going to need a method that takes in a top string, bottom string, and image source, and passes them off to the meme maker. Might save
#this image programatically, no clue how to do that
def memeMaker(topString,bottomString,URL):
    global i
    # going to start by opening firefox, but eventually I want all this automated
    memeURL = "https://memegen.link/custom/" +topString + "/" + bottomString + ".jpg?alt" "=" + URL #working but I've hardcoded the .jpg?alt part, no clue kinds of stuff I'll run into with this
    webbrowser.open_new(memeURL) #If your OS loads Edge as the default browser you need to take a break and rethink your life
    urllib.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "TestImage_" + i + ".jpg")
    i = i + 1 #python I love you but this makes me cry
    #ideally
#Method to split text into top and bottom meme? I don't know if its even worth the effort, maybe just for fun



#Main test stuff, this should be on top come on python why you gotta enforce ordering
picURL = picURLParser("https://twitter.com/RT_com/status/942156129961877504/photo/1")
memeMaker("i like", "really good memes", picURL)
