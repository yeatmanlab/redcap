# utils.py
# utility functions for RedCap scripts
# created by Patrick M. Donnelly
# April 5th, 2018



# apidelete_records
# this function performs the task of deleting records on RedCap using the API
# requirements: running the script delete_records.py
#               API token
# Input: record --> record_id as integer
# Output: none
def apidelete_records(record, token, redcap_path, buf):
    import pycurl,json,requests,sys,os
    import pandas as pd
    import numpy as np
    from io import BytesIO
    import utils

    data = [
        ('token', str(token)),
        ('action', 'delete'),
        ('content', 'record'),
        ('records[0]', str(record))
    ]

    ch = pycurl.Curl()
    ch.setopt(ch.URL, redcap_path)
    ch.setopt(ch.HTTPPOST, data)
    ch.setopt(ch.WRITEFUNCTION, buf.write)
    ch.perform()
#    ch.close()
#    buf.close()

    return;
