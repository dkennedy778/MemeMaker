# MemeMaker

Makes memes from tweets scraped from twitter. Use memeMaker.py to run, to change the input file modify line 5.

My input files were generated using taspinar's twitterscraper, any input files should be formatted similarly. I've included a sample query which was used to generate the data linked in my google drive 

This is a very early prototype, expect to find bugs, abherrent behavior, half finished features, and inexplicable design decisions.

Top level overview

The master memeMaker class instantiates the global logger, runs the JSON parser, and passes the parsed texts onto the makesMemes method. Note that you need to have a collection of unparsed tweets to run the program, sampleData.JSON is mine. This sample is too small to provide more than a few representative tweets. If you'd like to do a test run I've uploaded a larger sample file [here](https://drive.google.com/file/d/1SpggnFuU9O_kZJXX-MH0_I0Va_kKreGQ/view?usp=sharing).  

The JSONparser parses an input file containing many tweets. It searches specifically for tweets which could be considered "meme worthy". Right now, I define "meme Worthy" tweets as the following

1. The tweet has more than 20 retweets
2. The tweet has more than 4 words and less than 25
3. The tweet has some kind of image URL 
4. The tweet is in english 

These criteria are fluid and may change as I encounter more sample data. The above criteria will give me a pool of 3,500 tweets out of a sample of 1.5 million. 

The memeCompiler takes "memeWorthy" tweets and compiles them into a meme format. First it formats the text to remove any special characters(@,#,ect.), then splits the tweets text into a top and bottom portion. Then it takes the text and the tweets corresponding image and uses a memegen link to build the meme. Finally, it opens and downloads the memegen meme. 

The class also contains a picURLparser method, which will parse URLs out of pic.twitter links. 

The whole project uses a centralized logger to track errors. Error rates on image to meme conversion are relatively high, mostly caused by encoding errors.

Future development
1. Lower the error rate on tweet to meme conversion
2. Automate the process with a powershell script. Process should run tweetscraper, then run the master memeMaker class on the unparsed tweets.
3. Fine tune the requirements for "memeWorthy" tweets. Many of the outputted tweets are gibberish, could analyze tweets on characters (no tweets with # or @), length, or even something exotic like sentiment analysis
4. Use a DB to compress and store images. This will allow me to run the script continously without blowing up my hardrive 



