#Last name: Marchin
#First Name: Denis
#Student ID Number: 999061009
#CDF login id: g3dmarch
#Contact email address: d.marchin@mail.utoronto.ca 
#BlueMix credentials: username,password
#UG/Grad?: UG

#Last name: Chang
#First Name: Alex
#Student ID Number: 1000064681
#CDF login id: c2changk
#Contact email address: alexx.chang@mail.utoronto.ca  
#BlueMix credentials: username,password
#UG/Grad?: UG

#By submitting this file, I declare that my electronic submission is my
#own work, and is in accordance with the University of Toronto Code of
#Behaviour on Academic Matters and the Code of Student Conduct, as well
#as the collaboration policies of this course.

import csv, sys, re, sys, NLPlib
from HTMLParser import HTMLParser

# read in standard abbreviations file
f = open("abbrev.english")
abbrev = f.readlines()
f.close()

f2 = open("contractedwords")
conwords = f2.readlines()
f2.close()

# simple HTML code to ASCII converter
def html_to_acsii(text):
    hparser = HTMLParser()
    new_text = hparser.unescape(text)
    return new_text

# split tweet into sentences, one sentence per line.
def split_tweet(tweet):
    tweet = tweet.strip()
    processed = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", tweet) # create potential boundries

    i = 0
    while i < len(processed):                   # loop through words and check boundries
        words = processed[i].split(' ')
        if (len(processed) > i + 1):
            if ((words[-1] + '\n') in abbrev):
                new_word = processed[i] + " " + processed[i + 1]
                processed.pop(i)
                processed[i] = new_word
            if(words[-1][-1] == '!' or words[-1][-1] == '?'):
                temp = processed[i+1].split(' ')
                if temp[0].islower():
                    new_word = processed[i] + " " + processed[i + 1]
                    processed.pop(i)
                    processed[i] = new_word
        i = i + 1

    q = 0
    while q < len(processed):                   # strip trailing whitespace
        processed[q] = processed[q].strip()
        q = q + 1

    processed = "\n".join(processed)
    return processed

# split punctuations
def split_punc(tweet):
	processed = re.sub(r"([\w])([,.!;])", r"\1 \2", tweet)
	processed = re.sub(r"([,.!;])([\w])", r"\1 \2", processed)
	return processed

# split contracted words
def split_contracted(tweet):
	process = re.sub(r"(\w+(?=n't))(n't)", r"\1 \2", tweet) #split's word with its contraction, (ie: he'll -> he 'll)
	processed = re.sub(r"([^n])(')", r"\1 \2", process)  # split's contraction for special case "n't"
	return processed

# split the tweet into a list for tagging
def split_tolist(tweet):	
	processed = tweet.split()
	return processed

# tweet tagger
def tag(tweet):
	tagger = NLPlib.NLPlib()
	tags = tagger.tag(tweet)
	i = 0
	for tag in tags:
		tweet[i] = '{0}/{1}'.format(tweet[i], tag)
		i += 1
	return tweet

#get arguments
filepath = sys.argv[1]
group = sys.argv[2]
out = sys.argv[3]

f3 = open(filepath)
tweet_dump = csv.reader(f3)

# open a new file for writting
f4 = open(out, "w")

# go through cvs tweet entries
for ugly_tweet in tweet_dump:

    # get individual parts
    polarity = ugly_tweet[0]
    id = ugly_tweet[1]
    date = ugly_tweet[2]
    query = ugly_tweet[3]
    user = ugly_tweet[4]

    # text processing
    text = ugly_tweet[5].replace("/<[^>]+>/","")   # remove HTML tags and attrs
    text = html_to_acsii(text)                     # convert HTML codes to ASCII
    text = re.sub(r"http\S+", "", text)            # remove URLs
    text = text.replace('#', '')                   # remove hashtags
    text = text.replace('@', '')                   # remove @ before usernames
    text = split_tweet(text)

    text = split_punc(text)
    text = split_contracted(text)
    text = split_tolist(text)

    tags = tag(text)

    # write to file
    f4.write("<A=" + polarity + ">\n")

    i = 0
    for current in tags:
        f4.write(current + " ")
        if current == "./." and i != len(tags) - 1:
            f4.write("\n")
        i = i + 1
    f4.write("\n")




    
