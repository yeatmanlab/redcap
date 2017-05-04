# This script is designed to take any email script formatted according
# to the guidelines on the wiki and insert links extracted from REDCap
# repository into contact info from registry. To utilize, in the
# terminal, navigate to the folder containing this script and execute
# 'python email.py XXXX.txt' where XXXX.txt is the formatted form email
# ready for text insertion.
# 
# This script assumes that all subjects that have been exported from the
# registry need to receive the message that you are sending.

# Currently, repo_data is not being utilized for anything. Can be used
# to identify subjects that need to receive email. Or can change the
# target file that's being opened here and define these criteria in
# another script.

import pandas as pd
import sys
import subprocess
import numpy as np
import os
import glob

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# Find most recently exported files from registry and repository
reg_file = max(glob.iglob(home+'/Downloads/RDRPRegistry_DATA_*'), key=os.path.getctime)
repo_file = max(glob.iglob(home+'/Downloads/RDRPRepository_DATA_*'), key=os.path.getctime)
link_file = max(glob.iglob(home+'/Downloads/RDRPRepository_Participants_*'), key=os.path.getctime)

# Load data from each using record_id as index
reg_data = pd.read_csv(reg_file, index_col='record_id')
repo_data = pd.read_csv(repo_file, index_col='record_id')
link_data = pd.read_csv(link_file, skiprows=1, header=None, names=['dummy', 'na', 
    'record_id', 'd', 'e', 'f', 'survey', 'link'], index_col='record_id', dtype=object)
	
# Extract links for survey queues
reg_data['link'] = link_data.link

# And for survey
reg_data['survey'] = link_data.survey

# Import form letter passed in command line
form.read(sys.argv[1])


# def compose(ename, link, your):
# 	print 'Dear', ename + ', this is', your, 'link:', link
	
	
# Scrape subject data from info, input into form.format in the same order as the positions
# to be filled in.
for sub in reg_data.index:
    if pd.isnull(reg_data.parent_first_name[sub]):
        ename = reg_data.first_name[sub]
        link = reg_data.link[sub]
        your = 'your'
        body = form.format(ename=ename, link=link, your=your)
        email = reg_data.email[sub]
        print email
        subprocess.call('echo "{}" | mail -a "Content-Type: text/html" -s "{}" {} -aFrom:"Reading & Dyslexia Research Program<rdrp@uw.edu>"'.format(body, "Please complete the attached surveys", email), shell=True)
    else:
        ename = reg_data.parent_first_name[sub]
        link = reg_data.link[sub]
        your = reg_data.first_name[sub] + "'s"
        body = form.format(ename=ename, link=link, your=your)
        email = reg_data.email[sub]
        print email
        subprocess.call('echo "{}" | mail -a "Content-Type: text/html" -s "{}" {} -aFrom:"Reading & Dyslexia Research Program<rdrp@uw.edu>"'.format(body, "Please complete the attached surveys", email), shell=True)
    else: 
         print 'No email sent to', data.email[data.index[i]]
		
updated = pd.concat([data.redcap_event_name, data.survey_sent], axis=1)
updated.to_csv('~/Downloads/survey_sent.csv')