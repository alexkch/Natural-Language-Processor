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

from operator import add
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
def counter(tokens):

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

	for token in tokens:

		split_token = token.split("/")              # split token into the word and tag
		word = split_token[0]                       # actual word
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

		if word == "'ll" or word == "will" or word == "gonna":  #count easy future tense
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


def process(tokens):

    arffdict = counter(tokens)
    
    return arffdict.values()
    
def getclass(token):
	
	tweetclass = re.findall('\d+', token[0])
	return int(tweetclass[0])

def get_sentence_length(tokens):
	
	return len(tokens)


def get_token_length(tokens):
	
	token_lengths = []
	
	for token in tokens:
		split_token = token.split("/")              # split token into the word and tag
		token_lengths.append(len(split_token[0])) 
	
	return token_lengths

	
	
def output(fout, arff, tweetclass, sentences, sentence_len, token_len):

	print(tweetclass)
	avg_sentence_len = sum(sentence_len) / sentences
	avg_token_len = sum(token_len) / len(token_len)
	
	i = 0
	for current in arff:
		fout.write(str(current) + ",")
	fout.write(str(avg_sentence_len) + ",")
	fout.write(str(avg_token_len) + ",")
	fout.write(str(sentences) + ", ")
	fout.write(str(tweetclass) + "\n")
	
	return 0
		
		
#________MAIN____________________

input_file = sys.argv[1]
output_file = sys.argv[2]

f = open(input_file)
raw_data = f.readlines()
f_out = open(output_file, "w")

tweet = []
pattern = re.compile("<A=\d*>")
tweetclass = -1


arff = []
sentences = 0
sentence_len = []
token_len = []

for line in raw_data:                         
	tokens = line.split()                     
    
	if pattern.match(str(tokens[0])):       
		if tweetclass == -1:
			tweetclass = getclass(tokens)
			print(tweetclass)
		else:  #signifies the end of the tweet
			output(f_out, arff, tweetclass, sentences, sentence_len, token_len)
			arff = []
			sentences = 0
			sentence_len = []
			token_len = []
			tweetclass = getclass(tokens)
			print(tweetclass)
	else:
		if arff == []:
			arff = process(tokens)
			sentences += 1
			sentence_len.append(get_sentence_length(tokens))
			token_len.extend(get_token_length(tokens))
		else:
			new_arff = process(tokens)
			arff = map(add, arff, new_arff)
			sentences += 1
			sentence_len.append(get_sentence_length(tokens))
			token_len.extend(get_token_length(tokens))
			
output(f_out, arff, tweetclass, sentences, sentence_len, token_len) #last output as loop exits; it is needed
				


