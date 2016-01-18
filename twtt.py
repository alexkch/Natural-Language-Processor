#Last name: Marchin
#First Name: Denis
#Student ID Number: 999061009
#CDF login id: g3dmarch
#Contact email address: d.marchin@mail.utoronto.ca 
#BlueMix credentials: username,password
#UG/Grad?: UG

#By submitting this file, I declare that my electronic submission is my
#own work, and is in accordance with the University of Toronto Code of
#Behaviour on Academic Matters and the Code of Student Conduct, as well
#as the collaboration policies of this course.

import csv, sys, re, html.parser

# read in standard abbreviations file
f = open("abbrev.english")
abbrev = f.readlines()
f.close()

# simple HTML code to ASCII converter
def html_to_acsii(text):
    hparser = html.parser.HTMLParser()
    new_text = hparser.unescape(text)
    return new_text

# split tweet into sentences, one sentence per line.
def split_tweet(tweet):
    tweet = tweet.strip()
    processed = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", tweet) # create potential boundries

    i = 0
    while i < len(processed): # loop through words and check boundries
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
        else:
            return processed[0].strip()
        i = i + 1

    processed = "\n".join(processed)
    return processed


#get arguments
filepath = sys.argv[1]
#group = sys.argv[2]
#out = sys.argv[3]

f = open(filepath)
tweet_dump = csv.reader(f)

# go through cvs tweet entries
for ugly_tweet in tweet_dump:

    # get individual parts
    polarity = ugly_tweet[0]
    id = ugly_tweet[1]
    date = ugly_tweet[2]
    query = ugly_tweet[3]
    user = ugly_tweet[4]

    # processing

    text = ugly_tweet[5].replace("/<[^>]+>/","")   # remove HTML tags and attrs
    text = html_to_acsii(text)                     # convert HTML codes to ASCII
    text = re.sub(r"http\S+", "", text)            # remove URLs
    text = text.replace('#', '')                   # remove hashtags
    text = text.replace('@', '')                   # remove @ before usernames
    text = split_tweet(text)
    print(text)
#print(split_tweet("So much fun :-) There literally is an app for just about anything."))

