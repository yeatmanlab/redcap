#This script is designed to merge the registration info of an NLR subject with the data they already have in the repository.

# When run from the command line, this script will prompt you for the nlr_id of each subject, which can be looked up through the old NLR subject log (ask Patrick).

# This script completes all the same functions at the deindentify.py script, but also makes sure that subjects that were previously enrolled in the NLR study are matched up to their previous scores when their data is being transferred.

import pandas as pd
import numpy as np
import os
import glob

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# find the most recent data file exported from the screening database and set it as file_scr
file = max(glob.iglob(home+'/Downloads/RDRPScreeningDatabas_DATA_*'), key=os.path.getctime)

# load screening data using the record_id as the index
scr = pd.read_csv(file, index_col='record_id', dtype=object)

# Before changing record_id, set xfer values to complete
xfer = scr
xfer.reg_xfer=1
xfer.repo_xfer=1
xfer.scr_delete=1

# create new DataFrame to mark subs as transfered
xfer = pd.DataFrame(xfer, columns=['reg_xfer', 'repo_xfer', 'scr_delete'])

# load id_key using the record_id as the index
id_key = pd.read_csv(home+'/git/redcap/id_key.csv', dtype=object)

# Seed DataFrame for indexing
fixed_id=pd.DataFrame(columns=id_key.columns)
fixed_id.set_index('record_id', inplace=True)

# Create and mark column nlr_reg for later import into Repo
fixed_id.nlr_reg = '1'

# Index through subs and change record_id to match up to those with associated nlr_id
for sub in scr.index:
    # select the screening info for current sub
    temp_scr= scr.loc[scr.index==sub]
    # Request nlr_id for current sub
    nlr_input = input("Enter nlr_id for {} {}: ".format(scr.first_name[sub], scr.last_name[sub]))
    # select the id data from the id_key for this sub
    temp_id = id_key.loc[id_key['nlr_id']==nlr_input]
    # append the record_id from the temp_id
    temp_scr['record_id'] = temp_id.record_id[temp_id.index[0]]
    # set this record_id for the index in both
    temp_scr.set_index('record_id', inplace=True)
    temp_id.set_index('record_id', inplace=True)
    # combine this data
    comb_sub = pd.concat([temp_id, temp_scr], axis=1)
    fixed_id = fixed_id.append(comb_sub)

# Write test file
#fixed_id.to_csv('~/Desktop/test_nlr2.csv')


# create dummy email address for repository for ID
fixed_id['sid_email']=fixed_id.sid+'@red.cap'

# create new DataFrame for registry by selecting necessary values
reg = pd.DataFrame(fixed_id, columns=['child' , 'adult' ,
'teen' , 'who_complete' , 'xx' , 'are_you' , 'are_you_cap' , 'do_you'
, 'do_you_cap' , 'have_you' , 'have_you_cap' , 'i_' , 'i_cap' ,
'i_have' , 'i_have_cap' , 'my_data' , 'their' , 'their_cap' , 'v_s' ,
'were_you' , 'were_you_cap' , 'you' , 'you_cap' , 'you_and_your' ,
'you_and_your_cap' , 'you_are' , 'you_are_cap' , 'you_have' ,
'you_have_cap' , 'you_or_your' , 'you_or_your_cap' , 'your' ,
'your_cap' , 'screening_waiver_complete' , 'first_name' , 'last_name'
, 'dob' , 'scr_date' , 'age' , 'age_months' , 'gender' , 'teen_email'
, 'teen_phone' , 'parent_first_name' , 'parent_last_name' , 'email' ,
'phone' , 'city' , 'state' , 'zip' , 'parent2' , 'parent2_first_name'
, 'parent2_last_name' , 'parent2_email' , 'parent2_phone' , 'parent3'
, 'parent3_first_name' , 'parent3_last_name' , 'parent3_email' ,
'parent3_phone' , 'screening_complete' , 'scr_verified' ,
'verify_scr_complete' , 'gc_previous_data' , 'gc_future_data' ,
'gc_data_sharing_init' , 'gc_future_contact' , 'gc_family' ,
'gc_sub_agree' , 'gc_sub_sig' , 'gc_parent_agree' , 'gc_parent_sig' ,
'gc_date' , 'gc_lab' , 'gc_lab_date' , 'subject_id' , 'past_sub' , 'recruiting_status' , 'intervention_interest',
'general_consent_complete' , 'co_open' , 'co_datetime' , 'co_who' ,
'co_mode' , 'co_speak' , 'co_message' , 'co_email' , 'co_prefer' ,
'co_notes' , 'contact_complete' , 'email_name', 'redcap_event_name', 'sid'])

# create new DataFrame for repo
repo = pd.DataFrame(fixed_id, columns=['child' , 'adult' ,
'teen' , 'who_complete' , 'xx' , 'are_you' , 'are_you_cap' , 'do_you' ,
'do_you_cap' , 'have_you' , 'have_you_cap' , 'i_' , 'i_cap' , 'i_have' ,
'i_have_cap' , 'my_data' , 'their' , 'their_cap' , 'v_s' , 'were_you' ,
'were_you_cap' , 'you' , 'you_cap' , 'you_and_your' , 'you_and_your_cap'
, 'you_are' , 'you_are_cap' , 'you_have' , 'you_have_cap' ,
'you_or_your' , 'you_or_your_cap' , 'your' , 'your_cap' , 'dob' ,
'scr_date' , 'bilingual' , 'languages___1' , 'languages___2' ,
'languages___3' , 'languages___4' , 'languages___5' , 'languages___6' ,
'languages___7' , 'languages___8' , 'languages___9' , 'languages___10' ,
'languages___11' , 'languages___12' , 'languages___13' ,
'languages___14' , 'languages___15' , 'languages___16' ,
'languages___17' , 'languages___18' , 'languages___19' ,
'languages___20' , 'languages___21' , 'languages___98' ,
'languages_other' , 'primary_lang' , 'eng_age' , 'eng_daily' ,
'speech_dis' , 'speech_dis_dx___1' , 'speech_dis_dx___2' ,
'speech_dis_dx___3' , 'speech_dis_dx___4' , 'speech_dis_dx___5' ,
'speech_dis_dx___6' , 'speech_dis_dx___98' , 'speech_dis_other' ,
'speech_dis_treat' , 'aud_dis' , 'aud_dis_dx___1' , 'aud_dis_dx___2' ,
'aud_dis_dx___3' , 'aud_dis_dx___4' , 'aud_dis_dx___5' ,
'aud_dis_dx___98' , 'aud_dis_other' , 'aud_dis_treat' , 'dys_dx' ,
'dys_treat' , 'reading_rate' , 'adhd_dx' , 'ld_dx' , 'ld_treat' ,
'vision_dis' , 'brain_injury' , 'brain_injury_des' , 'brain_injury_cons'
, 'psych_dx' , 'meds' , 'scr_metal' , 'scr_mri' , 'screening_complete' ,
'scr_verified' , 'subject_id', 'redcap_event_name', 'sid', 'sid_email', 'nlr_reg'])

# write out csv files
reg.to_csv(home+'/Downloads/reg_nlr.csv')
repo.to_csv(home+'/Downloads/repo_nlr.csv')
xfer.to_csv(home+'/Downloads/xfer_nlr.csv')

# delete the file from which we're working for security!
os.remove(file)
