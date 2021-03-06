# ibmTrain.py
# 
# This file produces 11 classifiers using the NLClassifier IBM Service
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#

###IMPORTS###################################
#TODO: add necessary imports

import csv
import itertools
import re
import requests
import json
import codecs

###CONSTANTS#################################

input_csv_name = '/u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv'
url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"

username = "88992124-0531-4619-b710-ac512645af6a"
password = "7HOiCMuUwmKj"
file_size = [500, 2500, 5000]

###HELPER FUNCTIONS##########################

def partition(reader, gid):
    '''
    Partition the reader if a group number is given
    '''
    new_csv = []

    new_reader = list(reader)

    #first half
    idx1 = gid * 5500
    idx2 = ((gid + 1) * (5500 - 1))
    new_csv += new_reader[idx1:idx2]

    #second half
    idx1 = 800000 + gid * 5500
    idx2 = 800000 + ((gid + 1) * (5500 - 1))
    new_csv += new_reader[idx1:idx2]

    return new_csv

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
	# Converts an existing training csv file. The output file should
	# contain only the 11,000 lines of your group's specific training set.
	#
	# Inputs:
	#	input_csv - a string containing the name of the original csv file
	#		ex. "my_file.csv"
	#
	#	output_csv - a string containing the name of the output csv file
	#		ex. "my_output_file.csv"
	#`
	# Returns:
	#	None

	# open files
	
	f3 = open(input_csv_name)
	tweet_dump = partition(csv.reader(f3), group_id)
	f4 = open(output_csv_name, "w")
	for ugly_tweet in tweet_dump:

		polarity = ugly_tweet[0]
		text = ugly_tweet[5]

		text = text.replace("\"", '')
		text = text.replace("\t", "\\t")
		text = text.replace("\n", "\\n")
		text = text.replace("\r", "\\r")
		newline = (text + "," + polarity + '\n')
		f4.write(unicode(newline, errors='ignore'))	

	return
	
def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
	# Extracts n_lines_to_extract lines from a given csv file and writes them to 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	#	input_csv - a string containing the name of the original csv file from which
	#		a subset of lines will be extracted
	#		ex. "my_file.csv"
	#	
	#	n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
	#		ex. 500
	#
	#	output_file_prefix - a prefix for the output csv file. If unspecified, output files 
	#		are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
	#		The csv must be in the "watson" 2-column format.
	#		
	# Returns:
	#	None
	if n_lines_to_extract == 500:n = 500
	elif n_lines_to_extract == 2500: n = 2500
	elif n_lines_to_extract == 5000: n = 5000

	f = open(input_csv_file)
	fout = open(output_file_prefix + str(n) + ".csv", 'w')
	lines = f.readlines()
	for i in range(n_lines_to_extract):
		fout.write(lines[i])
	return
	
def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
	# Creates a classifier using the NLClassifier service specified with username and password.
	# Training_data for the classifier provided using an existing csv file named
	# ibmTrain#.csv, where # is the input parameter n.
	#
	# Inputs:
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	n - identification number for the input_file, as an integer
	#		ex. 500
	#
	#	input_file_prefix - a prefix for the input csv file, as a string.
	#		If unspecified data will be collected from an existing csv file 
	#		named 'ibmTrain#.csv', where # is the input parameter n.
	#		The csv must be in the "watson" 2-column format.
	#
	# Returns:
	# 	A dictionary containing the response code of the classifier call, will all the fields 
	#	specified at
	#	http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
	#   
	#
	# Error Handling:
	#	This function should throw an exception if the create classifier call fails for any reason
	#	or if the input csv file does not exist or cannot be read.

	training_metadata = {'language': 'en', 'name': 'nlc {}'.format(n)}
	data = {'training_metadata': json.dumps(training_metadata)} 

    # Open will throw an IOError Exception if the input file doesn't exist or can't be read
	with open('{}{}.csv'.format(input_file_prefix, n), 'r') as input_file:
		files = [('training_data', input_file)]
		response = requests.post(url, auth=(username, password), data=data, files=files)
        print(response.json())
        
	if not response.ok:
		raise Exception("The classifier could not be called")
    
	return response.json()

if __name__ == "__main__":
	
	#DO NOT CHANGE THE NAME OF THIS FILE
	output_csv_name = 'training_11000_watson_style.csv'
	
	convert_training_csv_to_watson_csv_format(input_csv_name, 88, output_csv_name)

	### STEP 2: Save 3 subsets in the new format into ibmTrain#.csv files
	extract_subset_from_csv_file(output_csv_name,500)
	extract_subset_from_csv_file(output_csv_name,2500)
	extract_subset_from_csv_file(output_csv_name,5000)
	
	### STEP 3: Create the classifiers using Watson
	for n in file_size:
		create_classifier(username, password, n, input_file_prefix='ibmTrain')

