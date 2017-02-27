# This script is meant to be run from the command line followed by the paths to the REDCap
# files that it is manipulating, in the order: links to survey queue, emails list, pending survey. 

import pandas as pd
import sys

links = pd.read_csv(sys.argv[1], skiprows=1, header=None, names=['dummy', 'na', 
	'record_id', 'd', 'e', 'f', 'g', 'link'], index_col='record_id')
	
emails = pd.read_csv(sys.argv[2], index_col='record_id')

sent = pd.read_csv(sys.argv[3], index_col='record_id')

merged = pd.concat([links['link'], emails, sent['survey_sent']], axis=1)

merged.to_csv('~/Downloads/merged.csv')