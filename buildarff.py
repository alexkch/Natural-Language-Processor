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

#get arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
f = open(input_file)
raw_data = f.readlines()

f_out = open(output_file, "w")
