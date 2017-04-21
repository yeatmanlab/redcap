# This script requires reports "Scheduling" to be downloaded most recently from Repo and Reg. Generates a file 'sched.csv' to import into reg.

import pandas as pd
import numpy as np
import os
import glob

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# find the most recent data file exported from the reg and repo and set it as the file
reg_file = max(glob.iglob(home+'/Downloads/RDRPRegistry_DATA_*'), key=os.path.getctime)
repo_file = max(glob.iglob(home+'/Downloads/RDRPRepository_DATA_*'), key=os.path.getctime)

# load data using the record_id as the index
reg = pd.read_csv(reg_file, index_col='record_id', dtype=object)
repo = pd.read_csv(repo_file, index_col='record_id', dtype=object)

# import time and get current time
from time import gmtime, strftime
now = strftime("%Y-%m-%d %H:%M", gmtime())

# find all subs with upcoming appointments
upcoming = pd.unique(repo.loc[repo['visit_dt'] >= now].index)

# change recruitment and past sub status of those without upcoming appointments
for sub in reg.index:
    if not sub in upcoming:
        if reg.ix[sub, 'recruiting_status'] == '2':
            reg.ix[sub, 'recruiting_status'] = 0
            reg.ix[sub, 'past_sub'] = 1

# set subs with upcoming appointments as scheduled             
for sub in upcoming:
    reg.loc[reg.index == sub, 'recruiting_status']=2
    reg.loc[reg.index == sub, 'past_sub'] = 1
   
# write out csv for upload to registry 
reg.to_csv(home+'/Downloads/sched.csv')