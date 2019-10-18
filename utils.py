# utils.py
# utility functions for RedCap scripts
# created by Patrick M. Donnelly
# April 5th, 2018



# apidelete_records
# this function performs the task of deleting records on RedCap using the API
# requirements: running the script delete_records.py
#               API token
# Input: record --> record_id as integer (integer)
#        token --> API token String (string)
#        redcap_path --> API url (string)
#        buf --> buffer variable (BytesIO)
# Output: none
def apidelete_records(record, token, redcap_path, buf):
    # import databases and modules
    import pycurl,json,requests,sys,os,certifi
    import pandas as pd
    import numpy as np
    from io import BytesIO
    import utils

    #format list command and input record from array passed from delete_records
    data = [
        ('token', str(token)),
        ('action', 'delete'),
        ('content', 'record'),
        ('records[0]', str(record))
    ]

    # send command to redcap
    ch = pycurl.Curl()
    ch.setopt(ch.CAINFO, certifi.where())
    ch.setopt(ch.URL, redcap_path)
    ch.setopt(ch.HTTPPOST, data)
    ch.setopt(ch.WRITEFUNCTION, buf.write)
    ch.perform()
    print('deleted',record)


    return;
