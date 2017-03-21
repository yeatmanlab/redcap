# This script is designed to take any email script formatted according to the guidelines
# on the wiki and insert data extracted from REDCap reg & repo. To utilize, in the terminal,
# navigate to the folder containing this script and execute 'python email.py XXXX.txt' where
# XXXX.txt is the formatted form email ready for text insertion.

# This script assumes that all subjects in the files exported from the repo require the 

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

# Load data from each using record_id as index
reg_data = pd.read_csv(reg_file, index_col='record_id')
repo_data = pd.read_csv(repo_file, index_col='record_id')

# Merge the two datasets
data = reg_data.combine_first(repo_data)

# Define the text of the email, using {} to indicate places to fill in
form = '''
Dear {},<br>
<br>
We appreciate your continued interest in the UW Reading & Dyslexia Research Program. Please use the link <a href="{}">here</a> to access a series of surveys and questionnaires. Each form is designed to be completed in only a few minutes.<br>
<br>
You can use this link to return to this list at any time and complete surveys at your leisure. The information provided will help us determine {} eligibility for current and future studies, as well as help us design future experiments and interventions.<br>
<br>
All questions are optional and you can choose not to provide any information that you do not feel comfortable sharing. If you have any questions, please respond to this email or call the lab at 206-685-9365.<br>
<br>
Please note that you will need to provide {} date of birth to access these surveys.<br>
<br>
Thank you for your time!<br>
Douglas Strodtman<br>
<br>
-- <br>
Douglas Strodtman<br>
Research Assistant<br>
<a href="http://depts.washington.edu/bdelab">Brain Development & Education Lab</a><br>
<a href="http://ilabs.washington.edu/">Institute for Learning & Brain Sciences (I-LABS)</a><br>
<br>
1715 Columbia Rd. N<br>
Portage Bay Building, #210<br>
University of Washington<br>
Seattle, WA, 98195<br>
<br>
(p): 206-685-9365<br>
(w): brainlab@uw.edu<br>
'''

# def compose(ename, link, your):
# 	print 'Dear', ename + ', this is', your, 'link:', link
	
	
# Scrape subject data from info, input into form.format in the same order as the positions
# to be filled in.
for i in range(len(data.index)):
		if data.survey_sent[data.index[i]] != 1:
			if pd.isnull(data.parent_first_name[data.index[i]]):
				ename = data.first_name[data.index[i]]
				link = data.link[data.index[i]]
				your = 'your'
				body = form.format(ename, link, your, your)
				email = data.email[data.index[i]]
				print email
				data.survey_sent[data.index[i]] = '1'
				subprocess.call('echo "{}" | mail -a "Content-Type: text/html" -s "{}" {} -aFrom:"Reading & Dyslexia Research Program<rdrp@uw.edu>"'.format(body, "Please complete the attached surveys", email), shell=True)
			else:
				ename = data.parent_first_name[data.index[i]]
				link = data.link[data.index[i]]
				your = data.first_name[data.index[i]] + "'s"
				body = form.format(ename, link, your, your)
				email = data.email[data.index[i]]
				print email
				data.survey_sent[data.index[i]] = '1'
				subprocess.call('echo "{}" | mail -a "Content-Type: text/html" -s "{}" {} -aFrom:"Reading & Dyslexia Research Program<rdrp@uw.edu>"'.format(body, "Please complete the attached surveys", email), shell=True)
		else: 
			print 'No email sent to', data.email[data.index[i]]
		
updated = pd.concat([data.redcap_event_name, data.survey_sent], axis=1)
updated.to_csv('~/Downloads/survey_sent.csv')