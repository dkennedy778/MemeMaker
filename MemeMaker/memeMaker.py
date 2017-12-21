from JSONParser import *
from MemeCompiler import *

#replace with loop
filename = 'sampleData.json'
tweetsToMeme = []
picURLs = []
tweetsToMeme, picURLs = parseMemes(filename)
makeMemes(tweetsToMeme, picURLs)