#!/usr/bin/env python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
#   Given some text and a dictionary set (indicated both as files), it returns a list of 
# candidate words with a confidence estimation for each. It supports entries of maximum 4 words.
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

def createDict(df):
    D = {}
    for idx, row in df.iterrows():
        word = row['value'].split(' ')
        n = len(word)
        if(n>0):
            e1 = D.get(word[0])
            if(e1 is None):
                D[word[0]] = {}
                if(n>1):
                    D[word[0]][word[1]] = {}
                    if(n>2):
                        D[word[0]][word[1]][word[2]] = {}
                        if(n>3):
                            D[word[0]][word[1]][word[2]][word[3]] = row['freq']
                        else:
                            D[word[0]][word[1]][word[2]] = row['freq']
                    else:
                        D[word[0]][word[1]]= row['freq']
                else:
                    D[word[0]] = row['freq']
            else:
                if(n>1):
                    e2 = e1.get(word[1])
                    if(e2 is None):
                        D[word[0]][word[1]] = {}
                        if(n>2):
                            D[word[0]][word[1]][word[2]] = {}
                            if(n>3):
                                D[word[0]][word[1]][word[2]][word[3]] = row['freq']
                            else:
                                D[word[0]][word[1]][word[2]] = row['freq']
                        else:
                            D[word[0]][word[1]]= row['freq']
                    else:
                        e3 = e2.get(word[2])
                        if(e3 is None):
                            D[word[0]][word[1]][word[2]] = {}
                            if(n>3):
                                D[word[0]][word[1]][word[2]][word[3]] = row['freq']
                            else:
                                D[word[0]][word[1]][word[2]] = row['freq']
                        else:
                            D[word[0]][word[1]][word[2]][word[3]] = row['freq']            
                else:
                    D[word[0]] = row['freq']
    return D


if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given some text and a dictionary set (indicated both as files), it returns a list of candidate words with a confidence estimation for each")
	parser.add_argument('-f','--folder',action="store", required=True, help="Directory with the text files to be scanned.")
	parser.add_argument('-d','--dictionary',action="store", required=True, help="Dictionary file.")
	args = parser.parse_args()

	##############################################################################################################################
	# Verify the existence of the directory with the labels
	if not os.path.isdir( args.folder ):
		print('\nERROR: Source folder', src_folder, 'does not exist.\n')
		parser.print_help()
		sys.exit(1)

	##############################################################################################################################
	# The existence of the dictionary is verified
	if ( not os.path.isfile( args.dictionary ) ):
		print('Error: Dictionary file was not found.\n')
		parser.print_help()
		sys.exit(2)
	##############################################################################################################################
	
	# The dictionary is built
	df = pd.read_csv( args.dictionary, names = ['value', 'freq'] )
	D = createDict( df )
	#print(D)

	# Go through each of the text files of the folder        
	for root, dirs, files in os.walk( args.folder ):
		for filename in files:
			if filename.endswith(".txt"):
				baseFilename = filename[:-4]
				start = datetime.datetime.now()	
			
				# Read the content of the text file, coverting it to unicode
				data = ''
				f = codecs.open( args.folder + '/' + filename, encoding='utf-8', mode='r')
				data = f.read().replace('\n', ' ').lower()
				f.close()
				#print(data)
				data = re.sub(' and | with | & |[,\.]', ' ', data)
				data = ' '.join( data.split() )
				data = data + " a a"
				#print(data)
				w1 = w2 = w3 = w4 = ''
				for w in data.split():
					w1 = w2
					w2 = w3
					w3 = w4
					w4 = w
		
					r1 = D.get(w1)
					if r1 is not None:
						if isinstance(r1, dict):
							r2 = r1.get(w2)
							if r2 is not None:
								if isinstance(r2, dict):
								    r3 = r2.get(w3)
								    if r3 is not None:
								        if isinstance(r3, dict):
								            r4 = r3.get(w4)
								            if r4 is not None:
								                if isinstance( r4, int ):
								                    print("N", baseFilename,w1,w2,w3,w4,str(r2))
								        elif isinstance( r3, int ):
								            print("N", baseFilename,w1,w2,w3,str(r3))
								elif isinstance( r2, int ):
								    print("N", baseFilename,w1,w2,str(r2))
						elif isinstance( r1, int ):
							print("N", baseFilename,w1,str(r1))
					
				end = datetime.datetime.now()
				diff = end - start
				print( "T", baseFilename, str(diff.total_seconds()) )		
				#sys.exit(3)		
