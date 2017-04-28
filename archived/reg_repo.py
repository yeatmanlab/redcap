# This script is meant to be run from the command line followed by the paths to the REDCap
# files that it is manipulating, in the order: registry file, repo file 

import pandas as pd
import sys

reg = pd.read_csv(sys.argv[1], index_col='record_id')
	
repo = pd.read_csv(sys.argv[2], index_col='record_id')

merged = pd.concat([reg, repo], axis=1)

merged.to_csv('~/Downloads/reg_repo.csv')