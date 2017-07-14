#!/usr/bin/python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
#   Given a text file with the structure name, string1, string2, it computes the similarity 
# for the strings of each row and prints back name, string1, string2, similarity.  
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
import sys, os, csv
import time
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance


def die_with_usage():
	""" HELP MENU """
	print ''
	print 'Usage:'
	print '   python strCompare.py <input_file>'
	print 'It assumes a file structure of name, string1, string2'
	print ''
	sys.exit(0)


if __name__ == '__main__':
	""" MAIN """
	# help menu
	if len(sys.argv) != 2:
		die_with_usage()

	# get params
	src_file = sys.argv[1]

	# sanity check
	if not os.path.isfile(src_file):
		print '\nERROR: source file', src_file, 'does not exist.\n'
		die_with_usage()
        
	f = open(src_file)
	reader = csv.reader(f)
	for line in reader:
		s = 1.0 - normalized_damerau_levenshtein_distance( line[1], line[2] )
		print line[0] + ',' + line[1] + ',' + line[2] + ',' + str(s)
	f.close() 

