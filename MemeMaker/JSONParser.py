#sample of json parsing methods to act as a foundation for future twitterscraping projects. Assuming data is formatted
#to twitterscraper's format

import json
from langdetect import detect
from urlextract import URLExtract
from pprint import pprint
import logging

JSONParser_logger = logging.getLogger('memeMaker')
namesList = []
substring_list = [".jpg","pic.twitter","imgur"]
def parseMemes(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        JSONParser_logger.info('loaded data file ' + str(data_file))
    picURLs = []
    memeTweets = []
    pprint("start")
    extractor = URLExtract()
    #Evaluating tweets on the following criteria 
    #1. The tweet has more than 20 retweets
    #2. The tweet has more than 4 words and less than 25
    #3. The tweet has some kind of image URL
    #4. The tweet is in english
    try:
        for dataPoint in data:
            if int(dataPoint["retweets"])> 20:
                s = str(dataPoint["text"])
                if(detect(s) == 'en'):
                    memeWorthy = len(s.split())  # splitting on whitespace
                    if memeWorthy < 25 and memeWorthy > 4: #does order impose performance cost?
                        if any(substring in s for substring in substring_list): #https://stackoverflow.com/questions/8122079/python-how-to-check-a-string-for-substrings-from-a-list
                            #loops through all URLs in the tweet until it finds the image one
                            urls = extractor.find_urls(s)
                            #HACK SOLUTION, need to alter a datastructure to allow for tweets that have 2+ picture URLs. This just includes the first
                            if urls: #poorly formatted tweets
                                for url in urls:
                                    if any(substring in url for substring in substring_list):
                                        #splitting the string to get ride of cases where the URL is more than just the pic.twitter link, probably should be doing this with regular expressions but whatever
                                        memeURLList = str(url).split("pic")
                                        picURL = "pic" + memeURLList[1]
                                        picURLs.append(picURL)
                                        memeTweets.append(dataPoint)
                                        break
                    #pprint(dataPoint)
    except Exception as e:
        JSONParser_logger.exception("exception hit")
    return (memeTweets, picURLs)
    #This is ok but we're still going to end up with a ton of trash. Could bounce over to the URL and use twitter's API to parse the comments
    #for reactions like "hahaha", "meme", "laughing emoji" or "lmao dead" or something. Then we queue each tweet by the chance its something
    #we can make into a meme, and give that to the maker first


#Other sample parsing methods

#first lets get the names of all users
#names = []
    # for dataPoint in data:
    # names.append(dataPoint["user"])
#cool, now let's be a bit more selective
# names.clear()
# for dataPoint in data:
#     likes= int(dataPoint["likes"])
#     if likes > 20:
#         names.append(dataPoint["user"])
#         #pprint(dataPoint) #I'm lazy

