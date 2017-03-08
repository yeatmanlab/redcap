# This script is designed to import data from merged.csv and output custom emails to each
# participant awaiting surveys in the RDRP. Assuming that merged.csv remains in the
# Downloads folder where it is currently being created, should run automatically

import pandas as pd
import sys
import subprocess

# Load merged data
data = pd.read_csv('~/Downloads/merged.csv', index_col='record_id')

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