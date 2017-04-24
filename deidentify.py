import pandas as pd
import numpy as np
import os
import glob

# set home directory so can be used on all OS
home = os.path.expanduser('~')

# find the most recent data file exported from the screening database and set it as the file
file = max(glob.iglob(home+'/Downloads/RDRPScreeningDatabas_DATA_*'), key=os.path.getctime)

# load data using the record_id as the index
scr = pd.read_csv(file, index_col='record_id', dtype=object)

# insert the redcap_event_name and set the value to subject_intake_arm_1 for easy import
scr['redcap_event_name'] = 'subject_intake_arm_1'

# set the sid from the subject_id
scr['sid']=scr.subject_id

# remove spaces from sid
for sub in scr.index:
    scr.loc[scr.index==[sub],'sid']=str(scr.sid[sub]).replace(" ", "")
    
# create dummy email address for repository for ID
scr['sid_email']=scr.sid+'@red.cap'

# create new DataFrame for registry by selecting necessary values
reg = pd.DataFrame(scr, columns=['child' , 'adult' ,
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
'gc_date' , 'gc_lab' , 'gc_lab_date' , 'subject_id' , 'past_sub' , 'recruiting_status' , 
'general_consent_complete' , 'co_open' , 'co_datetime' , 'co_who' ,
'co_mode' , 'co_speak' , 'co_message' , 'co_email' , 'co_prefer' ,
'co_notes' , 'contact_complete' , 'email_name', 'redcap_event_name', 'sid'])

# create new DataFrame for repo
repo = pd.DataFrame(scr, columns=['child' , 'adult' ,
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
'scr_verified' , 'subject_id', 'redcap_event_name', 'sid', 'sid_email'])

# set all transfer fields to complete
scr.reg_xfer=1
scr.repo_xfer=1
scr.scr_delete=1

# create new DataFrame to mark subs as transfered
xfer =pd.DataFrame(scr, columns=['reg_xfer', 'repo_xfer', 'scr_delete'])

# write out csv files
reg.to_csv(home+'/Downloads/reg.csv')
repo.to_csv(home+'/Downloads/repo.csv')
xfer.to_csv(home+'/Downloads/xfer.csv')

# delete the file from which we're working for security!
os.remove(file)