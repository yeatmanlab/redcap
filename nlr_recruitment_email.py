#!/usr/bin/env python3

''' This script is designed to take cleaned data from the old NLR subject log and compare it to data in the repository and registry to see who has registered and email invites to the rest of the subjects. 

Is your name Patrick Donnelly? If not, you probably should ask if he really wants you running this.

You will need to the following files in your downloads folder:

From the OneDrive account, download nlr_sublog.csv
From the Registry, download the report SIDs
From the Repository, download the report NLR Outreach
From the Repository, export the Survey Participant List (making sure that you have 'Unsubscribe' selected in the dropdown)

This script will schedule emails to be sent at 11pm to all NLR subjects that have not completed RDRP registration. IMPORTANT: if you have subjects marked in the screening database that haven't yet completed registration, you should manually delete them from the nlr_sublog.csv and reupload this file.
'''

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
sub_file = home+'/Downloads/nlr_sublog.csv'
link_file = max(glob.iglob(home+'/Downloads/RDRPRepository_Participants_*'), key=os.path.getctime)

# Load data
reg_data = pd.read_csv(reg_file, dtype=object)
repo_data = pd.read_csv(repo_file, index_col='nlr_id', dtype=object)
sub_data = pd.read_csv(sub_file, index_col='nlr_id')
link_data = pd.read_csv(link_file, skiprows=1, header=None, names=['dummy', 'na', 
    'record_id', 'd', 'e', 'f', 'unsubscribe', 'link'], index_col='record_id', dtype=object) # headers in the file are poorly written. na, d, e, f are all not used 

# Extract record_id from repo to sub_data
sub_data['record_id'] = repo_data.record_id

# And for sid
sub_data['sid'] = repo_data.sid

# Load the script to register NLR subs
form = open(home+'/git/redcap/email_temp/nlr_reg.txt')
form = form.read()
sys.stdout.write("NLR registration script loaded\n")

# Set subject line
 subl = 'Please register for our new database, the UW Reading & Dyslexia Research Program!'

# Set record_id as index for both sub and reg data (both are dtype object for comparison and floating concerns) & repo_data 
sub_data.set_index('record_id', inplace=True)
reg_data.set_index('record_id', inplace=True)
repo_data.set_index('record_id', inplace=True)

# Now that all are indexed by record_id, we can add other fields...
sub_data['unsubscribe']=link_data.unsubscribe

# Set the identity of the individual sending the email
lab_name = 'Patrick Donnelly'
lab_role = 'Graduate Research Assistant'

# Find intersection between sub and reg data (these are NLR subjects that have already registered)
overlap = sub_data.index.intersection(reg_data.index)

# Set these subs as having registered, then use this setting to match with other registered NLR subs
for sub in overlap:
    repo_data.nlr_reg[sub] = '1'
for sub in repo_data.index[repo_data.nlr_reg=='1']:
    sys.stdout.write('{} {} has already registered\n'.format(sub_data.first_name[sub], sub_data.last_name[sub]))

# Drop all these subs from the list to receive emails
sub_data.drop(repo_data.index[repo_data.nlr_reg=='1'], inplace = True)
sys.stdout.write('\nRegistered subjects will not receive emails\n')

# Capture today's date
today = time.strftime('%Y-%m-%d', time.localtime())

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

# set the start time as 11pm today, print this out to the command line
start_time_str = time.strftime('%d %b %y', time.localtime()) +' 23:00'
sys.stdout.write('Emails scheduled to send at ' + start_time_str +'\nIf this time is not tonight at 11pm, please exit script with Ctrl+C and troubleshoot\n')

# Convert this start_time to seconds since epoch to pass to sched
start_time = time.mktime(time.strptime(start_time_str, '%d %b %y %H:%M'))

# Create the scheduling object
s = sched.scheduler(time.time, time.sleep)

# Set an event with absolute time, which will delay rest of script until 11pm tonight
s.enterabs(start_time, 1, time.time, ())
s.run()



# Scrape subject data from info, input into form.format in the same order as the positions
# to be filled in.
for sub in sub_data.index: # We have already dropped subs that don't need to be contacted
    time.sleep(60) # add 60 second pause between emails
    if pd.isnull(sub_data.parent_first_name[sub]):
        ename = sub_data.first_name[sub]
        your = 'your'
        body = form.format(ename=ename, your=your, unsubscribe=sub_data.unsubscribe[sub], lab_name=lab_name, lab_role=lab_role)
        sub_email = sub_data.email[sub]
        
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
        
        # Record date email was sent for repo
        repo_data.nlr_email_date[sub] = today
        
        # update on status
        sys.stdout.write('Email sent to {} {}\n'.format(sub_data.first_name[sub], sub_data.last_name[sub]))
        
        # close server
        server.quit()
        
        # Write out updated repo_data csv each time in case script crashes
        repo_data.to_csv(home+'/Downloads/repo_nlr_reg.csv')
        
    else:
        ename = sub_data.parent_first_name[sub]
        your = sub_data.first_name[sub] + "'s"
        body = form.format(ename=ename, your=your, unsubscribe=sub_data.unsubscribe[sub], lab_name=lab_name, lab_role=lab_role)
        sub_email = sub_data.email[sub]
        
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
        
         # Record date email was sent for repo
        repo_data.nlr_email_date[sub] = today
        
        # update on status
        sys.stdout.write('Email sent to {} {}\n'.format(sub_data.first_name[sub], sub_data.last_name[sub]))

        # close server
        server.quit()
        
        # Write out updated repo_data csv each time in case script crashes
        repo_data.to_csv(home+'/Downloads/repo_nlr_reg.csv')

# Write out reminder to upload updated repository file
sys.stdout.write('\nPlease import repo_nlr_reg.csv to Repository\n')

# delete the files from which we're working for security!
os.remove(reg_file)
os.remove(repo_file)
os.remove(link_file)
os.remove(sub_file)
