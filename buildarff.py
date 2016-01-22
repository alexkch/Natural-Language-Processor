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
def count_pronouns(tokens):
    first_count = 0
    second_count = 0
    third_count = 0

    for token in tokens:
        split_token = token.split("\\")
        if split_token in first_person:
            first_count = first_count + 1
        elif split_token in second_person:
            second_count = second_count + 1
        elif split_token in third_person:
            third_count = third_count + 1
    return [first_count, second_count, third_count]

def process(tweet_lines):
    if tweet_lines == []:
        return '\n'

    return count_pronouns(tweet_lines)

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
        processed = process(tweet)                      # process tweet into meka format
        print(processed[1:])
        # f_out.write(processed)                        # write processed tweet to output file
        tweet = []                                      # clear current tweet.
        tweet.append(tokens)
    tweet.append(tokens)

