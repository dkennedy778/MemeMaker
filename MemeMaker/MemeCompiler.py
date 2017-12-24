#All the things related to meme generation, might have to split this up
#If I'm going to be fucking networking I need a logger service too
import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import re
import logging

#don't parse html with REGEX! https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags

MemeCompiler_logger = logging.getLogger('memeMaker')

#Going to need a method to follow a pic.twitter URL, find the actual image source, and return it to the user
def picURLParser(URL):
    page = requests.get("http://" +URL)
    if(page.status_code != 200):
        MemeCompiler_logger.warning('page failed to load for URL ' + URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    # ho boy I sure do hope twitter's image embedding is standardized
    pageData = soup.find(id="permalink-overlay")
    picData = pageData.find(class_="AdaptiveMediaOuterContainer")
    link = picData.find('img')
    URL = link.attrs['src'] #getting the wrong picture, gotta think about this some more
    return URL

#Going to need a method that takes in a top string, bottom string, and image source, and passes them off to the meme maker. Might save
#this image programatically, no clue how to do that

def memeMaker(topString,bottomString,URL):
    try:
        # going to start by opening firefox, but eventually I want all this automated
        parseMeBB = URL[0] + URL[1] + URL[2]
        #Removing tweets which are just images, likely superflorus after changes to JSONParser, test this
        if (topString == "" or bottomString == ""):
            return
        #Twitter picture URLs just take us to the tweet container for that picture. If we get there we need to parse the actual picture out of the tweet, which is handled by the URL parser
        if(parseMeBB == "pic"):
            nonTwitterURL = picURLParser(URL)
            memeURL = "https://memegen.link/custom/" +topString + "/" + bottomString + ".jpg?alt" "=" + nonTwitterURL #working, formatting issues abound
        else:
            memeURL = "https://memegen.link/custom/" + topString + "/" + bottomString + ".jpg?alt" "=" + URL
        memeURL = memeURL.replace('#',"") # Hashtags will cause link to fail, may be able to handle this in format text. Arguable that tweets containing hashtags aren't suitable for memes anyway
        webbrowser.open_new(memeURL) #If your OS loads Edge as the default browser you need to take a break and rethink your life
        filename = memeURL.split('/')[-1]
        req = urllib.request.Request(memeURL, headers={'User-Agent': "Magic Browser"})
        img = urllib.request.urlopen(req)
        localFile = open(filename,'wb')
        localFile.write(img.read())
        localFile.close()
        #webbrowser.close()
    except Exception as e:
        MemeCompiler_logger.exception("Failed to create and open memePage for " + URL)

#Method to split text into top and bottom meme? I don't know if its even worth the effort, maybe just for fun
def textSplitter(text):
    stringList = text.split()
    length = len(stringList)
    #I'm sure there's a better way to do this but this'll work. This way we know we're always getting whole words
    firstString = ""
    secondString = ""
    #round up or down?
    for x in range(0, int(length/2)):
        firstString += stringList[x] + " "
    for x in range(int(length/2), length):
        secondString += stringList[x] + " "
    splitString = [firstString,secondString]
    return splitString
#Need to strip text of anything and everything wacky, going to be a pain in the ass
def formatText(text):
    returnText = re.sub(r"http\S+", "", text)
    lazyBoi = re.sub(r"pic.twitter.com","",returnText)
    #re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    return lazyBoi
#Main test stuff, this should be on top come on python why you gotta enforce ordering
def makeMemes(tweets, PicURLs):
    try:
        i = 0
        for tweet in tweets:
            text = tweet["text"]
            formattedText = formatText(text)
            splitFormattedText = textSplitter(formattedText)
            picURL = PicURLs[i]
            memeMaker(splitFormattedText[0], splitFormattedText[1], PicURLs[i])
            i = i +1 #python why
    except Exception as e:
        MemeCompiler_logger.exception("Memecompiler hit an unexpected exception at tweet " + i )
