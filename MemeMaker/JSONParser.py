#sample of json parsing methods to act as a foundation for future twitterscraping projects. Assuming data is formatted
#to twitterscraper's format


import emoji #why does this exist
import json
from langdetect import detect
from urlextract import URLExtract
from pprint import pprint
import logging
import re

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
                if(text_has_no_emojis(s)):
                    if(detect(s) == 'en'):
                        memeWorthy = len(s.split())  # splitting on whitespace
                        if memeWorthy < 25 and memeWorthy > 4: 
                            if any(substring in s for substring in substring_list): #https://stackoverflow.com/questions/8122079/python-how-to-check-a-string-for-substrings-from-a-list
                                #loops through all URLs in the tweet until it finds the image one
                                urls = extractor.find_urls(s)
                                if urls: 
                                    for url in urls:
                                        if any(substring in url for substring in substring_list):
                                            #splitting the string to get ride of cases where the URL is more than just the pic.twitter link
                                            memeURLList = str(url).split("pic")
                                            picURL = "pic" + memeURLList[1]
                                            picURLs.append(picURL)
                                            memeTweets.append(dataPoint)
                                            break
    except Exception as e:
        JSONParser_logger.exception("exception hit")
    return (memeTweets, picURLs)

#This method sourced from https://gist.github.com/jezdez/0185e35704dbdf3c880f
#Checks to see if text has emojis, if it does the tweet is excluded 
def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI

def text_has_no_emojis(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return False
    return True

