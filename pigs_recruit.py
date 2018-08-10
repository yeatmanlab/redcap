# import necessary databases and libraries
import pycurl,json,requests,sys,os
import pandas as pd
import numpy as np
# existing redcap API stipulates StringIO, but pycurl now works with BytesIO
from io import BytesIO
# this is where the supplementary function apidelete_records() is stored
import utils

#where would you like the data to be stored
#this is initialized to the downloads to prevent storage on github repo
data_folder = os.path.expanduser('~/Downloads/')
desktop = os.path.expanduser('~/Desktop/')

token1_file = 'repo_apitoken.txt'
token2_file = 'reg_apitoken.txt'

if token1_file is not None:
    token1_path = os.path.join(desktop, token1_file)
    if os.path.exists(token1_path):
        with open(token1_path, 'r') as myfile:
            token1=myfile.read().replace('\n', '')
else:
    token1 = input('What is the repository API token? ')

if token2_file is not None:
    token2_path = os.path.join(desktop, token2_file)
    if os.path.exists(token2_path):
        with open(token2_path, 'r') as myfile:
            token2=myfile.read().replace('\n', '')
else:
    token2 = input('What is the registry API token? ')


# say which repository report you want
# report 25085 is the report in the repository called "PIGS Recruitment"
pigs_report = {
    'token': token1,
    'content': 'report',
    'format': 'csv',
    'report_id': '25085',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'csv'
}

# say which registry report you want
# report 12929 is the report in the registry  called "Emails"
emails_report = {
    'token': token2,
    'content': 'report',
    'format': 'csv',
    'report_id': '12929',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'csv'
}

redcap_path = 'https://redcap.iths.org/api/'
repo_list = requests.post(redcap_path, data=pigs_report)
emails = requests.post(redcap_path, data=emails_report)

repo_filename =os.path.join(data_folder,'pigs_repo.csv')

with open(repo_filename, 'w') as repo_file:
        repo_file.write(repo_list.text)

emails_filename = os.path.join(data_folder,'pigs_emails.csv')

with open(emails_filename, 'w') as email_file:
        email_file.write(emails.text)

pigs_repo_data = pd.read_csv(repo_filename)
email_data = pd.read_csv(emails_filename)


combined = pigs_repo_data.set_index('record_id').\
join(email_data.set_index('record_id'),
lsuffix='_repo', rsuffix='_reg')

combined.to_csv(os.path.join(data_folder,'combined.csv'))
