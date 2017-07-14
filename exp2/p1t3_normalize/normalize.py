#!/usr/bin/env python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: Given the result of getBySuffix.py, it search the candidate SNs in the 
# dictionary, and return the entry with the highest similarity. In order to be displayed, 
# the similarity must be higher than Threshold.
#   The similarity is computed using the normalized Damerau-Levenshtein distance. The 
# Damerau-Levenshtein library used is the developed by Geoffrey Fairchild and available at 
# https://github.com/gfairchild/pyxDamerauLevenshtein
##########################################################################################
# Copyright 2017    Advanced Computing and Information Systems (ACIS) Lab - UF
#                   (https://www.acis.ufl.edu/)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0.html
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################################
import os, sys, re, datetime
import argparse, numpy
import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

##############################################################################################################################################################
if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given the result of getBySuffix.py and a dictionary, search the candidates in the dictionary and returns their similarity")
	parser.add_argument('-i','--input',action="store", required=True, help="Text file to be scanned. Format: filename, scientific name, # of words, # matched characters")
	parser.add_argument('-d','--dictionary',action="store", required=True, help="Dictionary. ")
	parser.add_argument('-t','--threshold',action="store", required=False, type=float, default=0.8, help="Minimum similarity for a word to be accepted when compared to dictionary words.")
	args = parser.parse_args()

	##########################################################################################
	threshold = float(args.threshold)
	##########################################################################################
	# The existence of the source file is verified
	if ( not os.path.isfile( args.input ) ):
		print('Error: File does not exist.\n')
		parser.print_help()
		sys.exit(1)
	
	if ( not os.path.isfile( args.dictionary ) ):
			print('Error: Dictionary file does not exist.\n')
			parser.print_help()
			sys.exit(1)

	# Load the data 
	df_data = pd.read_csv( args.input, sep=',', names = ['filename', 'sname', 'nwords', 'nmatched'] )
	df_data.fillna('', inplace= True)
	
	# Load the dictionary
	df_dict = pd.read_csv( args.dictionary, sep=',', names = ['first', 'second'] )
	df_dict.fillna('', inplace= True)
	#print( df_dict.head(n=50) )
	##########################################################################################
	# Search each word in the firstname column (using similarity)
	for index, candidate in df_data.iterrows():
		firstname = ''
		secondname = ''
		
		p = candidate['sname'].partition(' ')
		n = 0
		if ( len(p) > 0 ):
			firstname =  p[0]
			n = 1
			if ( len(p) > 2 ):
				secondname = p[2]
				n = 2
				
		if n == 2:
			start = datetime.datetime.now()		
			for idx, entrada in df_dict.iterrows():
				sim1 = 1.0 - normalized_damerau_levenshtein_distance( firstname, entrada['first'] )
				if ( sim1 > threshold ):
					sim2 = 0.0
					if (secondname=='' and entrada['second'] == ''):
						sim2 = 1.0
					elif (secondname=='' and entrada['second'] != '') or (secondname!='' and entrada['second'] == ''):
						sim2 = 0.0
					else:
						sim2 = 1.0 - normalized_damerau_levenshtein_distance( secondname, entrada['second'] )
					if ( sim2 > threshold ):
						print( candidate['filename'], firstname, secondname, entrada['first'], entrada['second'], str( (sim1+sim2)/2 ))
			end = datetime.datetime.now()
			diff = end - start
			print( str(diff.total_seconds() * 1000) )					
					
