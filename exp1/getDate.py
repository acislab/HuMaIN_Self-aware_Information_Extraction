#!/home/user/anaconda3/bin/python
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
# Description: 
#   Given a text file as input, this script scans extracting dates, following the 
# format specified in the code. 
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

import sys, os, re, codecs
import pandas as pd

def die_with_usage():
	""" HELP MENU """
	print('')
	print('usage:')
	print('\tpython getDate.py /home/user/file.txt')
	print('')
	sys.exit(0)

####################################################################################################
# Regular expressions to be considered for day, month, and year
day = re.compile(r'\b(0?[1-9]|[12][\d]|3[01])\b')

month_word = re.compile(r'\b(january|february|march|april|may|june|july|august|september|october|november|december|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|jan|feb|mar|apr|may|jun|jul|aug|sep[t]?|oct|nov|dec|ene|abr|ago|dic)\b')
month_roman = re.compile(r'\b(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\b')
month_number = re.compile(r'\b([1-9]|10|11|12)\b')

year_long = re.compile(r'\b(1[89]\d\d|200[\d])\b')
year_short = re.compile(r'\b(\d\d)\b')

special = re.compile('[\W_]+')
####################################################################################################

dict_m = {'january':1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12, 'enero': 1, 'febrero': 2, 'marzo': 3, 'abril':4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12, 'ene': 1, 'abr': 4, 'ago': 8, 'sept': 9, 'dic': 12 }

####################################################################################################

def getDate( s ): # Return: isDate, month, day, year, length
	# Scan the whole string in search of dates
	w3, w2, w1, w0 = "", "", "", ""
	i=0
	df_output = pd.DataFrame( columns=('month', 'day', 'year') )
	for w in s.split():
		w3 = w2
		w2 = w1
		w1 = w0
		w0 = w
		
		# Year long
		y = year_long.match(w0)
		if (y != None):
			m = month_word.match(w1)
			if (m != None):  # Format day month_word year_long (12 febrero 2010)
				d = day.match(w2)
				if (d != None):
					df_output.loc[i] = [ m.group(0), d.group(0), y.group(0) ]
				else:			# Format month_word year_long (february 2010)
					df_output.loc[i] = [ m.group(0), '', y.group(0) ]
				i = i + 1
			else:
				m = month_word.match(w2)
				if (m != None): # Format month_word day year_long (february 12 2010)
					d = day.match(w1)
					if (d != None): 
						df_output.loc[i] = [ m.group(0), d.group(0), y.group(0) ]
						i = i + 1
				else:
					m = month_word.match(w3)  
					if (m != None): # Range of dates in the same month (feb 12 16 2010)
						d2 = day.match(w2)
						d1 = day.match(w1)
						if (d2 != None) and (d1 != None): 
							df_output.loc[i-1] = [ m.group(0), str(d2.group(0)) + ' ' + str(d1.group(0)), y.group(0) ]
					else:
						m = month_roman.match(w3)  
						if (m != None): # Range of dates in the same month (vii 12 16 2010)
							d2 = day.match(w2)
							d1 = day.match(w1)
							if (d2 != None) and (d1 != None): 
								df_output.loc[i-1] = [ m.group(0), str(d2.group(0)) + ' ' + str(d1.group(0)), y.group(0) ]
		else:
			# Year short
			y = year_short.match(w0)
			if (y != None):
				# 2 digits year must be converted, for comparison purposes, to four digits
				year_4d = str(1900 + int(y.group(0)))
				m = month_word.match(w1)
				if (m != None):  # Format day month_word year_long (12 febrero 10)
					d = day.match(w2)
					if (d != None):
						df_output.loc[i] = [ m.group(0), d.group(0), year_4d ]
						i = i + 1
				else:
					m = month_word.match(w2)
					if (m != None): # Format month_word day year_long (february 12 10)
						d = day.match(w1)
						if (d != None): 
							df_output.loc[i] = [ m.group(0), d.group(0), year_4d ]
							i = i + 1
					else:
						m = month_word.match(w3)  
						if (m != None): # Range of dates in the same month (feb 12 16 10)
							d2 = day.match(w2)
							d1 = day.match(w1)
							if (d2 != None) and (d1 != None): 
								df_output.loc[i-1] = [ m.group(0), str(d2.group(0)) + ' ' + str(d1.group(0)), year_4d ]
						else:
							m = month_roman.match(w3)  
							if (m != None): # Range of dates in the same month (vii 12 16 10)
								d2 = day.match(w2)
								d1 = day.match(w1)
								if (d2 != None) and (d1 != None): 
									df_output.loc[i-1] = [ m.group(0), str(d2.group(0)) + ' ' + str(d1.group(0)), year_4d ]				
						
	return i, df_output


if __name__ == '__main__':
	""" MAIN """
	# help menu
	if len(sys.argv) != 2:
		die_with_usage()

	# Text file validation
	src_file = sys.argv[1]
	if not os.path.isfile(src_file):
		print('\nERROR: source file', src_file, 'does not exist.\n')
		die_with_usage()

	# Read the content of the text file
	f = codecs.open(src_file, encoding='utf-8', mode='r')
	label = f.read().replace('\n', ' ').lower()
	f.close()
	
	# Eliminate special characters
	label = special.sub(' ', label)
	label = re.sub(' +', ' ', label)
	n_c, df_candidates = getDate( label )

	if ( n_c > 0 ):
		if n_c > 1:
			#for index, row in df_candidates.iterrows():
			df_candidates['m'] = df_candidates.apply (lambda row: dict_m[row['month']], axis=1)
			df_candidates = df_candidates.sort_values(by=['year', 'm', 'day'], ascending=[True, True, True])
		print( src_file.split('/')[-1][:-4] + ' ' + df_candidates['month'].iloc[0] + ' ' + str(df_candidates['day'].iloc[0]) + ' ' + df_candidates['year'].iloc[0]  )
