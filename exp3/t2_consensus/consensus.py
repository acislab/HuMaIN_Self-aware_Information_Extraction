#!/usr/bin/env python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
# 	Given a csv file with the columns: 'filename', 'value' it groups the values based on 
# filename and generates consensus. The winner is that of higher average similarity with 
# respect to the other options. 
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
			if s == 1.0: # Two identical values
				return i, 1.0
			sim[i] = sim[i] + s
			sim[j] = sim[j] + s
			j = j + 1	
		i = i + 1

	# Search maximum and save the index to return it
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
	parser.add_argument('-i','--input',action="store", required=True, help="csv file with the columns: filename, value")
	parser.add_argument('-o','--output',action="store", required=True, help="Name of the output file. Columns: filename, value, avg_sim")	
	args = parser.parse_args()

	# CRITERIA:
	# If two candidates have the same value, that is the winner and sim = 1. If there are no coincidences, 
	# the candidate with the highest average similarity is returned

	##########################################################################################
	# The existence of the source file is verified
	if ( not os.path.isfile( args.input ) ):
		print('Error: File does not exist.\n')
		parser.print_help()
		sys.exit(1)

	##########################################################################################
	# Read the file and load it in a DataFrame
	df = pd.read_csv( args.input, sep='\t', names = ['filename', 'value'] )

	##########################################################################################
	# C L E A N I N G 
	# Remove the null values from ocr_v and replace them with empty string
	df['value'].fillna('', inplace=True)
	# Replace 2 spaces by a single one
	df['value'] = df['value'].replace( {r'  ': ' '}, regex=True)
	# Remove all leading and trailing blanks in ocr_v and edit_v
	df['value'] = df['value'].map( lambda x: x.strip() )	
	
	##########################################################################################
	# Compute the Damerau Levenshtein similarity among the edit_v of each group
	groups_list = df.groupby(['filename'])
	
	dff = pd.DataFrame(columns=('filename', 'value', 'avg_sim'))
	i = 0
	for n, group in groups_list:
		w_id, w_sim = winner( group['value'].values )
		row = group[w_id:(w_id+1)][['filename', 'value']].values[0]
		row = numpy.append( row, w_sim )
		dff.loc[i] = row
		i = i + 1

	##########################################################################################
	# Save file to disk	
	dff = dff.sort_values( by='filename', ascending=1 )
	dff.to_csv( args.output, sep='\t', header = False, index = False )
