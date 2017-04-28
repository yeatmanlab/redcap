# Bash script to automatically add redcap_event_name column for import of screening data
# to repository

# Assign file to target .csv
file=$1

# Assign repo
repo=$'repo.csv'

# Delete if previous file exists
rm $repo

# Create repository csv
touch $repo

# Assign temp file
temp=$'temp.csv'

# Create temp file
touch $temp

# Find total number of rows
records=$(cat $file | wc -l)

# Prepare column in temp file
printf '%s\n' redcap_event_name $(i=2; while [ $i -le $records ]; do printf 'subject_intake_arm_1 '; i=$((i+1)); done) >> $temp

# Insert column into file, write out
paste -d, $file $temp >> $repo

# Delete temporary csv
rm $temp