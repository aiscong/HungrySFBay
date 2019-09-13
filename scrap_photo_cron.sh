#!/usr/bin/env bash

EMAIL="aiscong@gmail.com,jiwen.you.94@gmail.com"

HOME_PATH="$PWD"
TODAY=`date +"%Y%m%d"`

cd $HOME_PATH

if /Library/Frameworks/Python.framework/Versions/3.7/bin/python3 ${HOME_PATH}/main.py; then
    echo 'HungrySFBay scrap photo succeed at '$TODAY''
    mail -s "SUCCESS: HungrySFBay scrap photo" ${EMAIL} < /dev/null
else
    echo 'HungrySFBay scrap photo exited with error at '$TODAY''
    mail -s "FAILED: HungrySFBay scrap photo" ${EMAIL} < /dev/null
fi
