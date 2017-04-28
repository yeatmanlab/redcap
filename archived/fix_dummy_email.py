# Just a quick script to fix all the dummy emails so that surveys don't break

import pandas as pd
import numpy as np
import os
import glob

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# find the most recent data file exported from the screening database and set it as the file
file = max(glob.iglob(home+'/Downloads/RDRPRepository_DATA_*'), key=os.path.getctime)

# load data using the record_id as the index
repo = pd.read_csv(file, index_col='record_id', dtype=object)

# create dummy email address for repository for ID
repo['sid_email']=repo.sid+'@red.cap'

# write out results
repo.to_csv(home+'/Downloads/dummy_email.csv')