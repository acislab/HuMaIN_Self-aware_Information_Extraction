#!/usr/bin/env python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
#   Given a text file as input, this scripts search in it suffixes and combinations of these
# which can match a Scientific name (SN). It returns the candidate SNs and the length of 
# the matched suffixes.
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
import os, sys, codecs, re
import argparse
import pandas as pd

##############################################################################################################################################################
if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given some text and a group of suffixes (indicated both as files), it returns a list of candidate words with a confidence estimation for each")
	parser.add_argument('-i','--input',action="store", required=True, help="Text file to be scanned.")
	parser.add_argument('-s','--suffix',action="store", required=True, help="Text file with the values and list of suffixes.")	
	args = parser.parse_args()

	##########################################################################################
	# The existence of the source data file is verified
	if ( not os.path.isfile( args.input ) ):
		print('Error: Data file was not found.\n')
		parser.print_help()
		sys.exit(1)
	# The existence of the source file is verified
	if ( not os.path.isfile( args.suffix ) ):
		print('Error: Suffixes file was not found.\n')
		parser.print_help()
		sys.exit(2)
	##########################################################################################		
	# Read the suffixes in a file to a dictionary
	value = []
	suffix = []
	with open(args.suffix, 'r') as f_suffixes:
		for line in f_suffixes:
			line = line.strip()
			column = line.split(',')
			#print(len(column))
			if (len(column)>1):
				try:
					value.extend( [int( column[0] )] )
				except ValueError:
					print('Error: the first value of each line must be an integer indicating the value of the following suffixes.')
					parser.print_help()
					sys.exit(3)
				suffix.extend( [column[1:]] )

	##########################################################################################
	# Scan the text for groups of two words with the previous suffixes. Longer the suffix, longer the confidence
	df = pd.DataFrame( columns=['id', 'name', 'size', 'points'] )
	
	# Read the content of the text file, coverting to unicode
	f = codecs.open(args.input, encoding='utf-8', mode='r')
	data = f.read().replace('\n', ' ').lower()
	f.close()
	
	# Eliminate special characters
	pattern = re.compile('[\W_]+')
	data_lower = pattern.sub(' ', data)
	
	word1 = ''
	pts1 = 0
	n = 0	
	for word2 in data_lower.split():
		# Short word, not a scientific name
		if len(word2)<5:
			if (pts1 != 0): # 1 single word name
				df.loc[n] = [ n+1, word1, 1, pts1 ]
				n = n + 1
			pts1 = 0
			word1 = word2
			continue
			
		w2 = word2
		word2 = word2.lower()
		
		pts2 = 0
		for k in range( len(value) ):
			if pts2 == 0:
				for i in range(len( suffix[k] )):
					if word2.endswith( suffix[k][i] ):
						pts2 = value[k]
						break
		
		if (pts1 != 0):
			if (pts2 != 0):  # 2 words name
				df.loc[n] = [ n+1, word1 + ' ' + w2, 2, pts1 + pts2 ]
				pts1 = 0
				word1 = ''
			else: # 1 single word name
				df.loc[n] = [ n+1, word1, 1, pts1 ]
				pts1 = pts2
				word1 = w2
			n = n + 1
		else:
			pts1 = pts2
			word1 = w2					
	
	if (pts1 != 0):
		df.loc[n] = [ n+1, word1, 1, pts1 ]
		n = n + 1

	#print(df.to_string())
	filename = args.input.split('/')[-1]
	for index, row in df.iterrows():
		if (row['points'] >= 4) or ( (row['size']==1) and (row['points'] >= 3)):
			print( filename + ',' + row['name'] + ',' + str(int(row['size'])) + ',' + str(int(row['points'])) )

