#!/usr/bin/env python3

# This script is designed to take any email script formatted according
# to the guidelines on the wiki and insert links extracted from REDCap
# repository into contact info from registry.
 
# This script assumes that all subjects that have been exported from the
# repository need to receive the message that you are sending. Subs that are missing data in registry (whether just missing email or no record at all) will indicated as not receiving messages through command line feedback.

# import necessary modules
import smtplib
import pandas as pd
import os
import glob
import sys
import sched
import time
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
	
# Extract links for survey queues via innerjoin
reg_data = reg_data.join(link_data)

# Use the repo_data to select which individuals will receive emails
subs = pd.DataFrame(reg_data.ix[repo_data.index])

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

# Let user indicate which column to use to mark success of email being sent
if input('Would you like to mark a column in the repository that surveys have been sent? y/n ') == 'y':
    for column in repo_data.columns:
        sys.stdout.write(column+'\n')
    repo_col = input('Please type the name of the column you wish you mark: ')    
else:
    repo_col = None 

# Set all features not to be iterated
# Originating email
from_email = "rdrp@uw.edu"

# Set up html container to plug text into
body = """<html>
  <head></head>
  <body>
    <p>{}
    </p>
  </body>
</html>
"""

# Query for password and assign to variable
pswd = input('Please enter password for {}: '.format(from_email))

# Write out all subjects that have missing email data in reg
#no_email = repo_data[pd.isnull(subs['email'])]
#sys.stdout.write('\nNo email in reg for subjects:\n')
#for sub in no_email.index:
#    sys.stdout.write('{}\n'.format(no_email.sid[sub]))

# set the start time as 11pm today, print this out to the command line
start_time_str = time.strftime('%d %b %y', time.localtime()) +' 23:00'
sys.stdout.write('\nEmails scheduled to send at ' + start_time_str +'\nIf this time is not tonight at 11pm, please exit script with Ctrl+C and troubleshoot\n')

# Convert this start_time to seconds since epoch to pass to sched
start_time = time.mktime(time.strptime(start_time_str, '%d %b %y %H:%M'))

# Create the scheduling object
s = sched.scheduler(time.time, time.sleep)

# Set an event with absolute time, which will delay rest of script until 11pm tonight
s.enterabs(start_time, 1, time.time, ())
s.run()

# Scrape subject data from info, input into form.format in the same order as the positions
# to be filled in.
for sub in subs.index[pd.notnull(subs['email'])]: #excludes subs without email address defined
    time.sleep(60) # add 60 second pause between emails
    if pd.isnull(subs.parent_first_name[sub]):
        ename = subs.first_name[sub]
        link = subs.link[sub]
        your = 'your'
        body = form.format(ename=ename, link=link, your=your, unsubscribe=subs.survey[sub], lab_name=lab_name, lab_role=lab_role)
        sub_email = subs.email[sub]
        
        # Start server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, pswd)     
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['Subject'] = subl
        msg['From'] = from_email
        msg['To'] = sub_email
        
        # Create the body of the message.
        html = body.format(form)
        
        # Record the MIME types of text/html and attach into message container.
        msg.attach(MIMEText(html, 'html'))
        
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(from_email, sub_email, msg.as_string())
        
        # Mark that email has been sent (if told earlier) and write out (in case error)
        if repo_col:
            repo_data.loc[repo_data.index==[sub],repo_col]='1'
            repo_data.to_csv(home+'/Downloads/repo_email.csv')
        
        # update on status
        sys.stdout.write('Email sent to {}\n'.format(repo_data.sid.ix[sub]))
        
        # close server
        server.quit()
        
    else:
        ename = subs.parent_first_name[sub]
        link = subs.link[sub]
        your = subs.first_name[sub] + "'s"
        body = form.format(ename=ename, link=link, your=your, unsubscribe=subs.survey[sub], lab_name=lab_name, lab_role=lab_role)
        sub_email = subs.email[sub]
        
        # Start server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, pswd)
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['Subject'] = subl
        msg['From'] = from_email
        msg['To'] = sub_email
        
        # Create the body of the message.
        html = body.format(form)
        
        # Record the MIME types of text/html and attach into message container.
        msg.attach(MIMEText(html, 'html'))
        
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail(from_email, sub_email, msg.as_string())
        
        # Mark that email has been sent (if told earlier) and write out (in case error)
        if repo_col:
            repo_data.loc[repo_data.index==[sub],repo_col]='1'
            repo_data.to_csv(home+'/Downloads/repo_email.csv')
        
        # update on status
        sys.stdout.write('Email sent to {}\n'.format(repo_data.sid.ix[sub]))
        
        # close server
        server.quit()

# Reminder upload who has received email
if repo_col:
    sys.stdout.write('\nPlease import repo_email.csv to Repository\n')
        
# delete the files from which we're working for security!
os.remove(reg_file)
os.remove(repo_file)
os.remove(link_file)
