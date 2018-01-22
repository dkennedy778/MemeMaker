#All the things related to meme generation
import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import re
import logging

MemeCompiler_logger = logging.getLogger('memeMaker')

#Follows a tweet URL and parses out its corresponding image's source URL 
def picURLParser(URL):
    page = requests.get("http://" +URL)
    if(page.status_code != 200):
        MemeCompiler_logger.warning('page failed to load for URL ' + URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    pageData = soup.find(id="permalink-overlay")
    picData = pageData.find(class_="AdaptiveMediaOuterContainer") 
    link = picData.find('img')
    URL = link.attrs['src']
    return URL

#Removes nasty chars from tweet text. These either cause problems with URLs or look weird in memes
def removeChars(topString, bottomString):
    if '_' in topString:
       topString = topString.replace("_", " ")
    if '_' in bottomString:
        bottomString = bottomString.replace("_", " ")
    if '@' in topString:
        topString = topString.replace("@", " ")
    if '@' in bottomString:
        bottomString = bottomString.replace("@", " ")
    if '-' in topString:
        topString = topString.replace("-", " ")
    if '-' in bottomString:
        bottomString = bottomString.replace("-", " ")
    if '#' in topString:
        topString = topString.replace("#", " ")
    if '#' in bottomString:
        bottomString = bottomString.replace("#", " ")
    if '?' in topString:
        topString = topString.replace("?", " ")
    if '?' in bottomString:
        bottomString = bottomString.replace("?", " ")    
    return topString,bottomString

#Documented issues with memeMaker
#1. MemeGen really doesn't play well with chinese characters. Generally just won't display them, these shouldn't be getting past the language parser anyway

#2. 'https://memegen.link/custom/"Can you hear our song?" Some drawing based /off Calamari Inkantation, I hope you like it! /j8ZMAozgDd .jpg?alt=https://pbs.twimg.com/media/DRXXxEmX0AECbnB.jpg'
# This string realllyyy messed the parser up, tried to create a new meme for every single word in the sentence after song. Removing the question mark fixed it, seems like it functions as an escape character or something

#3. Seems like some tweets with videos are being passed through. Not really an issue since they just hit an exception but might be worth parsing out to save time later. At first glance picture and video links look identical,
#so if there's no easy way to do this I'll just let the encompassing try catch handle them

def memeMaker(topString,bottomString,URL):
    try:
        parseMeBB = URL[0] + URL[1] + URL[2]
        if (topString == "" or bottomString == ""):
            return

        #Remove characters unsuited for memes
        topString,bottomString = removeChars(topString,bottomString)

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

#Takes a meme's text and splits it into top and bottom portions
    stringList = text.split()
    length = len(stringList)
    #Split the text in two equal halves 
    firstString = ""
    secondString = ""
    for x in range(0, int(length/2)):
        firstString += stringList[x] + " "
    for x in range(int(length/2), length):
        secondString += stringList[x] + " "
    splitString = [firstString,secondString]
    return splitString
#Stripping text of malforming strings/link addresses. This method will be unified with removeChars
def formatText(text):
    returnText = re.sub(r"http\S+", "", text)
    lazyBoi = re.sub(r"pic.twitter.com","",returnText)
    #re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    return lazyBoi
#Main test loop
def makeMemes(tweets, PicURLs):
    try:
        i = 0
        for tweet in tweets:
            text = tweet["text"]
            formattedText = formatText(text)
            splitFormattedText = textSplitter(formattedText)
            memeMaker(splitFormattedText[0], splitFormattedText[1], PicURLs[i])
            i = i +1 #python why
    except Exception as e:
        MemeCompiler_logger.exception("Memecompiler hit an unexpected exception at tweet " + i )

