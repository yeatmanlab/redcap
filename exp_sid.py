import pandas as pd
import numpy as np
import os
import glob

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# find the most recent data file exported from the screening database and set it as the file
file = max(glob.iglob(home+'/Downloads/RDRPScreeningDatabas_DATA_*'), key=os.path.getctime)

# load data using the record_id as the index
scr = pd.read_csv(file, index_col='record_id')

# insert the redcap_event_name and set the value to subject_intake_arm_1 for easy import
scr['redcap_event_name'] = 'subject_intake_arm_1'

# overwrite sid_1
for sub in scr.index:
	temp = scr.sid_1[sub]
	if temp == 0:
		new = 'Z'
	elif temp == 1:
		new = 'A'
	elif temp == 2:
	    new = 'B'
	elif temp == 3:
		new = 'C'
	elif temp == 4:
		new = 'D'
	elif temp == 5:
		new = 'E'
	elif temp == 6:
		new = 'F'
	elif temp == 7:
		new = 'G'
	elif temp == 8:
		new = 'H'
	elif temp == 9:
		new = 'I'
	elif temp == 10:
		new = 'J'
	elif temp == 11:
		new = 'K'
	elif temp == 12:
		new = 'L'
	elif temp == 13:
		new = 'M'
	elif temp == 14:
		new = 'N'
	elif temp == 15:
		new = 'O'
	elif temp == 16:
		new = 'P'
	elif temp == 17:
		new = 'Q'
	elif temp == 18:
		new = 'R'
	elif temp == 19:
		new = 'S'
	elif temp == 20:
		new = 'T'
	elif temp == 21:
		new = 'U'
	elif temp == 22:
		new = 'V'
	else:
	    new = ''
	scr.loc[scr.index==[sub],'sid_1'] = new

# overwrite sid_2
for sub in scr.index:
	temp = scr.sid_2[sub]
	if temp == 96:
		new = 'A'
	elif temp == 0:
		new = 'B'
	else:
	    new = ''
	# This list will need to be fleshed out if this script is to be maintained.
	scr.loc[scr.index==[sub],'sid_2'] = new
		
# hack together sid
for sub in scr.index:
	scr.loc[scr.index==[sub],'sid']='{}{}{}'.format(scr.sid_1[sub],scr.sid_2[sub],sub)
	
# create dummy email address for repository for ID
scr['sid_email']=scr.sid+'@red.cap'

# Create dataframe for sid and sid_email:
exp = pd.DataFrame(scr, columns=['redcap_event_name','sid','sid_email'])

# write out csv files
exp.to_csv(home+'/Downloads/exp_sid.csv')