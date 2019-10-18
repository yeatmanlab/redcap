#delete_records.property
# Patrick M. Donnelly, April 5, 2018
# script to delete records in screening database of RedCap
# please make sure you are sure you are deleting the correct people as per IRB
# requires: API token from admin member

# import necessary databases and libraries
import json,requests,sys,os, pycurl, certifi
import pandas as pd
import numpy as np
# existing redcap API stipulates StringIO, but pycurl now works with BytesIO
from io import BytesIO
# this is where the supplementary function apidelete_records() is stored
import utils

# ask user for api token
# if you need an access token, consult the RedCap API page
# only users with admin (delete) priveleges will be able to use this script
token = input('What is the API token? ')

# initialize the buffer to communicate with http framework
buf = BytesIO()

# say which report you want
# report 13128 is the report in the screening database called "Delete"
report = {
    'token': token,
    'content': 'report',
    'format': 'csv',
    'report_id': '13128',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'csv'
}
# specify API address
redcap_path = 'https://redcap.iths.org/api/'
# use requests module to pull data from database using api token
# and convert to csv
to_delete = requests.post(redcap_path, data=report)
home = os.path.expanduser('~')
report_filename =os.path.join(home+'/Downloads/deleteme.csv')
with open(report_filename, 'w') as report_file:
        report_file.write(to_delete.text)
delete_report = pd.read_csv(report_filename)
# look at only the record_id field
records = delete_report['record_id']
# intialize empty array and loop through individually deleting records in that
# array
delete_me = []
for record in range(0,records.size):
    # function call to apidelete_records in utils folder
    utils.apidelete_records(records[record], token, redcap_path, buf)
#ch.close()
buf.close()

# overwrite API token
token = []
