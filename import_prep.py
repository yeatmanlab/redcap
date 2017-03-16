import pandas as pd
import numpy as np

# load data
data = pd.read_csv('/Users/douglasstrodtman/Downloads/nlr.csv')

# find unique subs that need sid
need_sids = pd.isnull(data.sid)
	
# set indexing for sid_num to 1
sid_num = 1

# this replaces all the first visit undefined sids with 'foo'
for sub in data.index[need_sids]:
    if data.Visit[sub] == 1:
        if data.Age[sub] < 60:
            sid1 = 'D'
        elif data.Age[sub] < 72:
            sid1 = 'E'
        elif data.Age[sub] < 84:
            sid1 = 'F'
        elif data.Age[sub] < 96:
            sid1 = 'G'
        elif data.Age[sub] < 108:
            sid1 = 'H'
        elif data.Age[sub] < 120:
            sid1 = 'I'
        elif data.Age[sub] < 132:
            sid1 = 'J'
        elif data.Age[sub] < 144:
            sid1 = 'K'
        elif data.Age[sub] < 156:
            sid1 = 'L'
        elif data.Age[sub] < 168:
            sid1 = 'M'
        elif data.Age[sub] < 216:
            sid1 = 'N'
        elif data.Age[sub] < 300:
            sid1 = 'O'
        elif data.Age[sub] < 420:
            sid1 = 'P'
        elif data.Age[sub] < 540:
            sid1 = 'Q'
        elif data.Age[sub] < 660:
            sid1 = 'R'
        elif data.Age[sub] < 780:
            sid1 = 'S'
        elif data.Age[sub] < 900:
            sid1 = 'T'
        elif data.Age[sub] < 1020:
            sid1 = 'U'
        else:
            sid1 = 'V'
        sid_full = '{}A{}'.format(sid1,str(sid_num).zfill(3))
        data.loc[data.Subject==data.Subject[sub],'sid']=sid_full
        sid_num += 1

# work with visit nums
data.insert(4, 'redcap_event_name', 0, allow_duplicates=False)
for viz in data.index:
    data.loc[data.index==[viz],'redcap_event_name']='visit_{}_arm_1'.format(int(data.Visit[viz]))


# now to deal with the formatting of the column names; code isn't perfect, but gets job done
for old in range(len(data.columns.values)):
    new = data.columns.values[old]
    data.columns.values[old] = new.lower()

# write to csv
data.to_csv('~/Downloads/import.csv')
        
# select all instances of a subject and replace sids with foo for now
# for sub in pd.unique(data.Subject[need_sids]):
# 	data.loc[data.Subject==sub,'sid']='foo'
# 
# intakes = data.Age[data.Visit==1]
# 
# data[data['Visit'] == 1]
# 
# data.ix[0,['Subject','Visit']]


