#!/usr/bin/env python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
# 	Given a csv file with the columns: id, id_e_l, id_v, specimen_n, filename, ocr_v, edit_v,
# it generates an output file with the consensus winner and similarity for the available 
# edit_v for an specimen. The winner is that of hhigher average similarity with respect to 
# the other options. 
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
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################################

import os, sys, csv
import argparse, numpy
import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

##############################################################################################################################################################
def winner( v_ ):
	n = v_.size
	sim = [0.0] * n
	
	if n == 1: return 0, 1.0
		
	i = 0
	while(i < n):
		j = i + 1
		while(j < n):
			s = 1.0 - normalized_damerau_levenshtein_distance( v_[i], v_[j] )
			sim[i] = sim[i] + s
			sim[j] = sim[j] + s
			j = j + 1	
		i = i + 1

	# Search maximum and return the index
	sim_max = sim[0]
	i_max = 0
	i = 1
	while(i < n):
		if (sim_max < sim[i]):
			i_max = i
			sim_max = sim[i]
		i = i + 1
		
	return i_max, (sim_max/(n-1))
##############################################################################################################################################################
##############################################################################################################################################################
if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Generate consensus winner from a crowdsourced field.")
	parser.add_argument('-i','--input',action="store", required=True, help="csv file with the columns: id, id_e_l, id_v, specimen_n, filename, ocr_v, edit_v")
	parser.add_argument('-o','--output',action="store", required=True, help="Name of the output file. Columns: 'filename', 'edit_v', 'ocr_v', 'avg_sim'")	
	args = parser.parse_args()

	# CRITERIA:
	# Given the set of values available for each scientific name, the script will compute the similarity of each candidate with 
	# all the other candidate, accumulating the similarity values. The candidate with the highest similarity value will be the winner.
	# If two candidates have the same cumulative similarity, the first candidate with that similarity will be picked up.

	##########################################################################################
	# The existence of the source file is verified
	if ( not os.path.isfile( args.input ) ):
		print 'Error: File does not exist.\n'
		parser.print_help()
		sys.exit(1)

	##########################################################################################
	# Read the file and load it in a DataFrame
	df = pd.read_csv( args.input, names = ['id', 'id_e_l', 'id_v', 'specimen_n', 'filename', 'ocr_v', 'edit_v'] )

	##########################################################################################
	# C L E A N I N G 
	# Remove the null values from ocr_v and replace them with empty string
	df['ocr_v'].fillna('', inplace=True)
	df['edit_v'].fillna('', inplace=True)
	# Remove the newline characters and replace them with single space
	df['ocr_v'] = df['ocr_v'].replace( {r'\r': ' ', r'\n': ' '}, regex=True)
	df['edit_v'] = df['edit_v'].replace( {r'\r': ' ', r'\n': ' '}, regex=True)	
	# Replace 2 spaces by a single one
	df['ocr_v'] = df['ocr_v'].replace( {r'  ': ' '}, regex=True)
	df['edit_v'] = df['edit_v'].replace( {r'  ': ' '}, regex=True)	
	# Remove all leading and trailing blanks in ocr_v and edit_v
	df['ocr_v'] = df['ocr_v'].map( lambda x: x.strip() )
	df['edit_v'] = df['edit_v'].map( lambda x: x.strip() )	
	
	##########################################################################################
	# Compute the Damerau Levenshtein similarity among the edit_v of each group
	groups_list = df[['id','specimen_n','filename','ocr_v','edit_v']].groupby(['specimen_n'])
	
	dff = pd.DataFrame(columns=('filename', 'edit_v', 'ocr_v', 'avg_sim'))
	i = 0
	for n, group in groups_list:
		w_id, w_sim = winner( group['edit_v'].values )
		row = group[w_id:(w_id+1)][['filename', 'edit_v', 'ocr_v']].values[0]
		row = numpy.append( row, w_sim )
		dff.loc[i] = row
		i = i + 1

	##########################################################################################
	# Save file to disk	
	dff = dff.sort_values( by='filename', ascending=1 )
	dff.to_csv( args.output, sep='\t', header = False, index = False )
