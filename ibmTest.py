# ibmTest.py
# 
# This file tests all 11 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#		You may also find it helpful to reuse some of your functions from ibmTrain.py.
#

###IMPORTS##############################################################

import csv, requests, re, json, urllib

# Disable warnings
requests.packages.urllib3.disable_warnings()

###CONSTANTS############################################################

url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/"
test_data = '/u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv'


######### CREDENTIALS ##################################################
#username = "03f335cf-dbac-4f6f-8a82-211813430928"
#password = "h6UjcleAHAKs"


######### NEW ##########################################################
username = "88992124-0531-4619-b710-ac512645af6a"
password = "7HOiCMuUwmKj"

file_size = [500, 2500, 5000]

##############################################

def get_classifier_ids(username,password):
	# Retrieves a list of classifier ids from a NLClassifier service 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#		
	# Returns:
	#	a list of classifier ids as strings
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason
	#
    
	response = requests.get(url, data={}, auth=(username, password))	
	ids = []
	for classifier in response.json()['classifiers']:
		ids.append(classifier['classifier_id'])
	
	if not response.ok:
		raise Exception("get Classifier call failed.")
        
	return ids
	

def assert_all_classifiers_are_available(username, password, classifier_id_list):
	# Asserts all classifiers in the classifier_id_list are 'Available' 
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id_list - a list of classifier ids as strings
	#		
	# Returns:
	#	None
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason AND 
	#	It should throw an error if any classifier is NOT 'Available'
	#
	
	unavaliable = []
	not_ready = ''
	
	for classifier in classifier_id_list:
		response = requests.get(url + classifier, data={}, auth=(username, password))
		
		# if the status is not avaliable, add it to unavaliable list
		if str(response.json()['status']) != 'Available':
			unavaliable.append(classifier)
	
	# if there are classifiers unavaliable, raise exception
	if len(unavaliable) > 0:
	
		for status in unavaliable:
			not_ready = not_ready + ' ' + status 
	
		raise Exception ("classifier(s):" + not_ready + " is/are not ready")
	
	return

def classify_single_text(username,password,classifier_id,text):
	# Classifies a given text using a single classifier from an NLClassifier 
	# service
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id - a classifier id, as a string
	#		
	#	text - a string of text to be classified, not UTF-8 encoded
	#		ex. "Oh, look a tweet!"
	#
	# Returns:
	#	A "classification". Aka: 
	#	a dictionary containing the top_class and the confidences of all the possible classes 
	#	Format example:
	#		{'top_class': 'class_name',
	#		 'classes': [
	#					  {'class_name': 'myclass', 'confidence': 0.999} ,
	#					  {'class_name': 'myclass2', 'confidence': 0.001}
	#					]
	#		}
	#
	# Error Handling:
	#	This function should throw an exception if the classify call fails for any reason 

	classification = {}		
	
	# encode the text into utf-8 for query
	query = urllib.quote(text.encode("utf-8"))
	
	# throws exception if call fails
	response = requests.get(url + classifier_id + "/classify?text=" + query, auth=(username, password))
    
	if not response.ok:
		raise Exception("Classifier call failed.")

	classification['top_class'] =  response.json()['top_class']
	classification['classes'] = response.json()['classes']

	return classification
	


def classify_all_texts(username,password,input_csv_name):
        # Classifies all texts in an input csv file using all classifiers for a given NLClassifier
        # service.
        #
        # Inputs:
        #       username - username for the NLClassifier to be used, as a string
        #
        #       password - password for the NLClassifier to be used, as a string
        #      
        #       input_csv_name - full path and name of an input csv file in the 
        #              6 column format of the input test/training files
        #
        # Returns:
        #       A dictionary of lists of "classifications".
        #       Each dictionary key is the name of a classifier.
        #       Each dictionary value is a list of "classifications" where a
        #       "classification" is in the same format as returned by
        #       classify_single_text.
        #       Each element in the main dictionary is:
        #       A list of dictionaries, one for each text, in order of lines in the
        #       input file. Each element is a dictionary containing the top_class
        #       and the confidences of all the possible classes (ie the same
        #       format as returned by classify_single_text)
        #       Format example:
        #              {classifiername:
        #                      [
        #                              {'top_class': 'class_name',
        #                              'classes': [
        #                                        {'class_name': 'myclass', 'confidence': 0.999} ,
        #                                         {'class_name': 'myclass2', 'confidence': 0.001}
        #                                          ]
        #                              },
        #                              {'top_class': 'class_name',
        #                              ...
        #                              }
        #                      ]
        #              , classifiername2:
        #                      [
        #                            
        #                      ]
        #              
        #              }
        #
        # Error Handling:
        #       This function should throw an exception if the classify call fails for any reason
        #       or if the input csv file is of an improper format.
        #
	
	class_dict = {}
	all_texts = []
	
	try:
		fp = open(input_csv_name)
	
	except IOError:
		print("Error opening file")
		sys.exit()

	with fp:	

		data = list(csv.reader(fp))

		#get classifier ids has an error handler inside the function to handle classify call fails
		classifier_ids = get_classifier_ids(username, password)
		
		for classifier in classifier_ids:
			class_dict[classifier] = []
		
		for rawtext in data:

			#obtain the tweets from rawtext
			text = rawtext[5]

			#classify_single_text handles errors to classify_calls inside
			for classifier2 in classifier_ids:
				class_dict[classifier2].append(classify_single_text(username, password, classifier2, text))

		return class_dict


def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the accuracy of this
	# classifier according to the input csv file
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	
	correct_hit = 0
	index = 0
	
	try:
		fp = open(input_csv_file_name)
	
	except IOError:
		print("Error opening file")
		sys.exit()

	with fp:

		data = list(csv.reader(fp))
		
		for line in data:
			if int(classifier_dict[index]["top_class"]) == int(line[0]):
				correct_hit += 1
			index += 1

		accuracy = correct_hit / float(len(classifier_dict))
		
		return accuracy

def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the average 
	# confidence of this classifier wrt the selected class, according to the input
	# csv file. 
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The average confidence of the classifier, as a number between [0.0-1.0]
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should thr	#STEP 1: Ensure all 11 classifiers are ready for testing
	
	#STEP 2: Test the test data on all classifiers
	
	#STEP 3: Compute the accuracy for each classifier
	
	#STEP 4: Compute the confidence of each class for each classifierow an error if there is an issue with the 
	#	inputs.
	#
	
	#TODO: fill in this function
	correct = 0.0
	incorrect = 0.0
	correctTotal = 0
	incorrectTotal = 0
	
	index = 0
	
	try:
		fp = open(input_csv_file_name)
	
	except IOError:
		print("Error opening file")
		sys.exit()

	with fp:

		data = list(csv.reader(fp))
		
		for line in data:
			
			if int(classifier_dict[index]["top_class"]) == int(line[0]): #sprediction is correct
				correctTotal += 1
				correct += float(classifier_dict[index]["classes"][0]["confidence"])
				index += 1
			else:
				incorrectTotal += 1
				incorrect += float(classifier_dict[index]["classes"][0]["confidence"])
				index += 1
			
		conf_correct = correct/correctTotal
		conf_incorrect = incorrect/incorrectTotal
		
		return (conf_correct, conf_incorrect)

if __name__ == "__main__":

	# get classifier ids, error checking inside function
	classifier_ids = get_classifier_ids(username, password)
	
	
	# assert that all classifiers are avaliable, error checking within function itself
	assert_all_classifiers_are_available(username, password, classifier_ids)
	
	classifier_dict = classify_all_texts(username, password, test_data)

	try:
		f = open("4output.txt", 'w')
	except IOError:
		print("Error opening file")
		sys.exit()

	with f:
	
		for classifier in classifier_ids:

			accuracy = compute_accuracy_of_single_classifier(classifier_dict[classifier], test_data)
			confidence = compute_average_confidence_of_single_classifier(classifier_dict[classifier], test_data)
		
			line = str(classifier) + "accuracy: " + str(accuracy) + "confidence: " + str(confidence) +  '\n'
			f.write(line)
