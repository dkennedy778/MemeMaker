#sample of json parsing methods to act as a foundation for future twitterscraping projects. Assuming data is formatted
#to twitterscraper's format

import json

from pprint import pprint

namesList = []
substring_list = [".jpg","pic","imgur"]

with open('sampleData.json') as data_file:
    data = json.load(data_file)
    #pprint(data)
#first lets get the names of all users
names = []
for dataPoint in data:
    names.append(dataPoint["user"])
#cool, now let's be a bit more selective
names.clear()
for dataPoint in data:
    likes= int(dataPoint["likes"])
    if likes > 20:
        names.append(dataPoint["user"])
        #pprint(dataPoint) #I'm lazy
#Ok, lets try figuring out what we'd want for a meme
#Want to limit the number of sentences, or maybe the amount of text. For now we'll just limit ourselves to two sentences
#also going to want an image somewhere in the picture, that's a bit tougher. Will start by looking for image extensions or tags from sites like imgur
#Only looking for successful memes, so we're limiting ourselves to at least 20 retweets. Not sure exactly what's the sweet number here
#but I'm going to prioritize propensity to share content over plain "likes".
names.clear()
memeTweets = []
for dataPoint in data:
    #Well for starters how do we count the number of sentences? ("..." is going to fuck up a split)
    #Start by just counting words, that probably matters more anyway. Might want to remove any non-consecutive periods anyway
    if int(dataPoint["retweets"])> 20:
        s = dataPoint["text"]
        memeWorthy = len(s.split())  # splitting on whitespace
        if memeWorthy < 50: #does order impose performance cost?
            if any(substring in s for substring in substring_list): #https://stackoverflow.com/questions/8122079/python-how-to-check-a-string-for-substrings-from-a-list
                memeTweets.append(dataPoint)
                pprint(dataPoint)
    #This is ok but we're still going to end up with a ton of trash. Could bounce over to the URL and use twitter's API to parse the comments
    #for reactions like "hahaha", "meme", "laughing emoji" or "lmao dead" or something. Then we queue each tweet by the chance its something
    #we can make into a meme, and give that to the maker first

