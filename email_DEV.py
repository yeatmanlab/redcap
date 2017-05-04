#!/usr/bin/env python3

# This script is designed to take any email script formatted according
# to the guidelines on the wiki and insert links extracted from REDCap
# repository into contact info from registry.
 
# This script assumes that all subjects that have been exported from the
# registry need to receive the message that you are sending.

# Currently, repo_data is not being utilized for anything. Can be used
# to identify subjects that need to receive email. Or could change the
# target file that's being opened here and define these criteria in
# another script.

# import necessary modules
import smtplib
import pandas as pd
import os
import glob
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# Find most recently exported files from registry and repository
# (please note that one could also easily modify script to specify files you wish to use, but as we're trying to minimize RDRP data that's stored on machines, requiring download immediately before and then automating deletion within this script facilitates that end goal)
# reg_file should be report XX
# repo_file should be report XX
# link_file should be downloaded from XX as according to wiki
reg_file = max(glob.iglob(home+'/Downloads/RDRPRegistry_DATA_*'), key=os.path.getctime)
repo_file = max(glob.iglob(home+'/Downloads/RDRPRepository_DATA_*'), key=os.path.getctime)
link_file = max(glob.iglob(home+'/Downloads/RDRPRepository_Participants_*'), key=os.path.getctime)

# Load data from each using record_id as index
reg_data = pd.read_csv(reg_file, index_col='record_id')
repo_data = pd.read_csv(repo_file, index_col='record_id')
link_data = pd.read_csv(link_file, skiprows=1, header=None, names=['dummy', 'na', 
    'record_id', 'd', 'e', 'f', 'survey', 'link'], index_col='record_id', dtype=object) # headers in the file are poorly written. na, d, e, f are all not used 
	
# Extract links for survey queues
reg_data['link'] = link_data.link

# And for survey
reg_data['survey'] = link_data.survey

# Check to make sure we are sending surveys
# Script is set up to take any text formatted according to rules published on wiki
if input('Would you like to send out the survey queue? y/n ') == 'y':
    form = open(home+'/git/redcap/email_temp/survey.txt')
    form = form.read()
    sys.stdout.write("Survey script loaded\n")
else:
    sys.stdout.write('Select one of the following templates:\n')
    os.system('ls '+home+'/git/redcap/email_temp')
    selection = input('Which of the above templates would you like to load? ')
    form = open(home+'/git/redcap/email_temp/'+selection)
    form = form.read()
    sys.stdout.write(selection+' loaded\n\n')
	
# Check to see what subject line should be used, then set
subl_sel = input('Please select a subject line for your message:\n(1) Please complete the attached surveys\n(2) Greetings from the UW Reading & Dyslexia Research Program\n(3) New study opportunity with the UW Reading & Dyslexia Research Program\n(4) Custom\nPlease enter the number of your choice: ')
if subl_sel == '1':
    subl = 'Please complete the attached surveys'
elif subl_sel == '2':
    subl = 'Greetings from the UW Reading & Dyslexia Research Program'
elif subl_sel == '3':
    subl = 'New study opportunity UW Reading & Dyslexia Research Program'
else:
    subl = input('Please enter text for email Subject line: ')

# Set the identity of the individual sending the email
lab_name = input('Please enter the name to be used in the signature: ')
lab_role = input('Please enter the title of this individual: ')

# Set all features not to be iterated
# Originating email
rdrp_email = "rdrp@uw.edu"

# Set up html container to plug text into
body = """\
<html>
  <head></head>
  <body>
    <p>{}
    </p>
  </body>
</html>
"""

# Start server and query for password
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(rdrp_email, input('Please enter password for rdrp@uw.edu: '))

# Scrape subject data from info, input into form.format in the same order as the positions
# to be filled in.
for sub in reg_data.index:
    if pd.isnull(reg_data.parent_first_name[sub]):
        ename = reg_data.first_name[sub]
        link = reg_data.link[sub]
        your = 'your'
        body = form.format(ename=ename, link=link, your=your, survey=reg_data.survey[sub], lab_name=lab_name, lab_role=lab_role)
        sub_email = reg_data.email[sub]
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['Subject'] = subl
        msg['From'] = rdrp_email
        msg['To'] = sub_email
        
        # Create the body of the message.
        html = body.format(form)
        
        # Record the MIME types of text/html and attach into message container.
        msg.attach(MIMEText(html, 'html'))
        
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(rdrp_email, sub_email, msg.as_string())
    else:
        ename = reg_data.parent_first_name[sub]
        link = reg_data.link[sub]
        your = reg_data.first_name[sub] + "'s"
        body = form.format(ename=ename, link=link, your=your, survey=reg_data.survey[sub],  lab_name=lab_name, lab_role=lab_role)
        sub_email = reg_data.email[sub]
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['Subject'] = subl
        msg['From'] = rdrp_email
        msg['To'] = sub_email
        
        # Create the body of the message.
        html = body.format(form)
        
        # Record the MIME types of text/html and attach into message container.
        msg.attach(MIMEText(html, 'html'))
        
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(rdrp_email, sub_email, msg.as_string())
	
# updated = pd.concat([data.redcap_event_name, data.survey_sent], axis=1)
# updated.to_csv('~/Downloads/survey_sent.csv')