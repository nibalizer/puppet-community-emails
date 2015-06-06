#!/bin/bash

# Script to create the monthly stats email for puppet-community

source venv/bin/activate

email_file=emails/puppet_community_stats-`date +%F`.txt

if [ -f $email_file ]; then
    echo "Email file already exists, cowardly refusing to continue"
    echo "Email file: $email_file"
    exit 1
fi


cat share/greeting.txt >> $email_file
echo "Date: $(date +%F)" >> $email_file
echo "" >> $email_file

python user_stats.py >> $email_file
echo "" >> $email_file
python repo_stats.py >> $email_file
echo "" >> $email_file
python comment_stats.py >> $email_file

echo "" >> $email_file

# Community Mgmt repo comes from Morgan++
./community_management/pull_requests.rb -t `cat config.py | grep token | cut -d "=" -f 2 |tr -d '"'` -n puppet-community


cat share/closing.txt >> $email_file


