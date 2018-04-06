#delete_records.property
# Patrick M. Donnelly, April 5, 2018
# script to delete records in screening database of RedCap
# please make sure you are sure you are deleting the correct people as per IRB
# requires: API token from admin member

import pycurl,json,requests,sys,os
import pandas as pd
import numpy as np
from io import BytesIO
import utils

token = input('What is the API token? ')

buf = BytesIO()

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

redcap_path = 'https://redcap.iths.org/api/'
to_delete = requests.post(redcap_path, data=report)

home = os.path.expanduser('~')
report_filename =os.path.join(home+'/Downloads/deleteme.csv')

with open(report_filename, 'w') as report_file:
        report_file.write(to_delete.text)
delete_report = pd.read_csv(report_filename)

records = delete_report['record_id']

delete_me = []
for record in range(0,records.size):
    utils.apidelete_records(records[record], token, redcap_path, buf)
    print('deleted',records[record])
ch.close()
buf.close()
