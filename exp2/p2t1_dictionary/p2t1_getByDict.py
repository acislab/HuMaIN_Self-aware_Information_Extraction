#!/usr/bin/env python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
#   Scans a text file for matches with the entries of a dictionary. It returns the entries 
# ans values which similarity is higher than Threshold.  
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
import os, sys, re, codecs, datetime
import argparse, numpy
import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

##############################################################################################################################################################
if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given some text and a dictionary set (indicated both as files), it returns a list of candidate words with a confidence estimation for each")
	parser.add_argument('-i','--input',action="store", required=True, help="Text file to be scanned.")
	parser.add_argument('-d','--dictionary',action="store", required=True, help="Dictionary file.")
	parser.add_argument('-t','--threshold',action="store", required=False, type=float, default=0.85, help="Minimum similarity for a word to be accepted when compared to dictionary words.")
	args = parser.parse_args()

	start = datetime.datetime.now()
	##########################################################################################
	threshold = float(args.threshold)
	##########################################################################################
	# The existence of the source data file is verified
	if ( not os.path.isfile( args.input ) ):
		print('Error: Label file was not found.\n')
		parser.print_help()
		sys.exit(1)
	# The existence of the dictionary is verified
	if ( not os.path.isfile( args.dictionary ) ):
		print('Error: Dictionary file was not found.\n')
		parser.print_help()
		sys.exit(2)
	##########################################################################################		
	# Load the dictionary
	df_dict = pd.read_csv( args.dictionary, sep=',', names = ['first', 'second'] )
	df_dict.fillna('', inplace= True)
	##########################################################################################
	# Scan the text for groups of two words of length greater than or equal to 5
	
	# Read the content of the text file, coverting to unicode
	f = codecs.open(args.input, encoding='utf-8', mode='r')
	data = f.read().replace('\n', ' ').lower()
	f.close()

	# Eliminate special characters
	pattern = re.compile('[\W_]+')
	data_lower = pattern.sub(' ', data)

	firstname = ''
	n = 0	
	for secondname in data_lower.split():
		if ( (len(firstname)>4) and (len(secondname)>4) ): # two long words
		
			for idx, entrada in df_dict.iterrows():	
				sim1 = 1.0 - normalized_damerau_levenshtein_distance( firstname, entrada['first'] )
				if ( sim1 > threshold ):
					sim2 = 1.0 - normalized_damerau_levenshtein_distance( secondname, entrada['second'] )
					if ( sim2 > threshold ):
						print( args.input, firstname, secondname, entrada['first'], entrada['second'], str( (sim1+sim2)/2 ))
	
		firstname = secondname

	end = datetime.datetime.now()
	diff = end - start
	print( args.input, str(diff.total_seconds()) )					
			
