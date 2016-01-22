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

import csv, sys, re, sys

# feature categories

first_person = ["I", "me", "my", "mine", "we", "us", "our", "ours"]
second_person = ["you", "your", "yours", "u", "ur", "urs"]
third_person = ["he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"]
common_nouns = ["NN", "NNS"]
proper_nouns = ["NNP", "NNPS"]
adverbs = ["RB", "RBR", "RBS"]
wh_words = ["WDT", "WP", "WP$", "WRB"]
slang = ['smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff', 'wyd', 'lylc', 'brb',
         'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl', 'imo', 'ltr', 'thx', 'kk', 'omg',
         'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr', 'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru',
         'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol']

# super mega counter
def counter(tweet_list):

    counts = {'first': 0,
              'second': 0,
              'third': 0,
              'conjunctions': 0,
              'past_tense':0,
              'future_tense':0,
              'commas':0,
              'colons':0,
              'dashes':0,
              'parentheses':0,
              'ellipsis':0,
              'common':0,
              'proper':0,
              'adverbs':0,
              'wh':0,
              'slang':0,
              'upper':0 }

    for line in tweet_list:
        for token in line:
            split_token = token.split("/")              # split token into the word and tag
            word = split_token[0]                       # actual word
            if word == '\n': continue                   # if new line char, skip it.

            tag = split_token[1]                        # assigned tag

            # check pronouns
            if word in first_person:                    # check if word is a first person pronoun
                counts['first'] = counts['first'] + 1
            elif word in second_person:                 # check if word is a second person pronoun
                counts['second'] = counts['second'] + 1
            elif word in third_person:                  # check if word is a third person pronoun
                counts['third'] = counts['third'] + 1

            if tag == "CC" :
                counts['conjunctions'] = counts['conjunctions'] + 1 # count coordinating conjunctions

            if tag == "VBD" :
                counts['past_tense'] = counts['past_tense'] + 1     # count past tense

            if word == "'ll" or word == "will" or word == "gonna":  # count easy future tense
                counts['future_tense'] = counts['future_tense'] + 1

            # if word == "going": # start check for hard future tense
            #     idx = line.index[split_token]
            #     if line[idx+1] == 'to' and line[idx+2].split("/")[1] == "VB":
            #         counts['future_tense'] = counts['future_tense'] + 1

            if word == "," :
                counts['commas'] = counts['commas'] + 1         # count commas

            if word == ";" or word == ":" :
                counts['colons'] = counts['colons'] + 1         # count colons and semicolons

            if word == "-" :
                counts['dashes'] = counts['dashes'] + 1         # count dashes

            if word == "..." :
                counts['ellipsis'] = counts['ellipsis'] + 1     # count ellipsis

            if tag in common_nouns:
                counts['common'] = counts['common'] + 1         # count common nouns

            if tag in proper_nouns:
                counts['proper'] = counts['proper'] + 1         # count proper nouns

            if tag in adverbs:
                counts['adverbs'] = counts['adverbs'] + 1       # count adverbs

            if tag in wh_words:
                counts['wh'] = counts['wh'] + 1                 # count wh words

            if word in slang:
                counts['slang'] = counts['slang'] + 1           # count slang words

            if word == word.upper():
                counts['upper'] = counts['upper'] + 1           # count all uppercase words

    return counts

def process(tweet_lines):
    if tweet_lines == []:
        return '\n'

    polarity = tweet_lines[0]
    count = counter(tweet_lines[1:])
    return count.values()

#get arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
f = open(input_file)
raw_data = f.readlines()
f_out = open(output_file, "w")

tweet = []
for line in raw_data:                                   # loop through lines
    tokens = line.split(" ")                            # seperate lines into tokens

    if line == '<A=4>\n' or line== '<A=0>\n':           # look for start of new tweet
        processed = process(tweet[1:])                      # process tweet into meka format
        print(processed)
        # f_out.write(processed)                        # write processed tweet to output file
        tweet = []                                      # clear current tweet.
        tweet.append(tokens)
    tweet.append(tokens)

