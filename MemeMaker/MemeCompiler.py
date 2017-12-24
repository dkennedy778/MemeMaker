import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import re
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#don't parse html with REGEX! https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags


#Opens the tweet containing the picture and parses its URL out using BS4
def picURLParser(URL):
    page = requests.get("http://" +URL)
    if(page.status_code != 200):
        print("requests failed")
    soup = BeautifulSoup(page.content, 'html.parser')
    # ho boy I sure do hope twitter's image embedding is standardized
    pageData = soup.find(id="permalink-overlay")
    picData = pageData.find(class_="AdaptiveMediaOuterContainer")
    link = picData.find('img')
    URL = link.attrs['src'] 
    return URL

#Going to need a method that takes in a top string, bottom string, and image source, and passes them off to the meme maker.
def memeMaker(topString,bottomString,URL):
    try:
        # going to start by opening firefox, but eventually I want all this automated
        parseMeBB = URL[0] + URL[1] + URL[2]
        #Removing tweets which are just images, likely superflorus after fixes to JSONParser, test this
        if (topString == "" or bottomString == ""):
            return
        if(parseMeBB == "pic"):
            nonTwitterURL = picURLParser(URL)
        memeURL = "https://memegen.link/custom/" +topString + "/" + bottomString + ".jpg?alt" "=" + nonTwitterURL #working, formatting issues abound
        memeURL = memeURL.replace('#',"") # Hashtags will cause link to fail, may be able to handle this in format text. Arguable that tweets containing hashtags aren't suitable for memes anyway
        webbrowser.open_new(memeURL) #If your OS loads Edge as the default browser you need to take a break and rethink your life
        filename = memeURL.split('/')[-1]
        req = urllib.request.Request(memeURL, headers={'User-Agent': "Magic Browser"})
        img = urllib.request.urlopen(req)
        localFile = open(filename,'wb')
        localFile.write(img.read())
        localFile.close()
        #webbrowser.close()
    except:
        print("s")

#Method to split text into top and bottom to fit into the meme
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
#Need to strip text of anything and everything wacky
def formatText(text):
    returnText = re.sub(r"http\S+", "", text)
    lazyBoi = re.sub(r"pic.twitter.com","",returnText)
    #re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    return lazyBoi
#Main method
def makeMemes(tweets, PicURLs):
    i = 0
    for tweet in tweets:
        text = tweet["text"]
        formattedText = formatText(text)
        splitFormattedText = textSplitter(formattedText)
        picURL = PicURLs[i]
        memeMaker(splitFormattedText[0], splitFormattedText[1], PicURLs[i])
        i = i +1 #python why

