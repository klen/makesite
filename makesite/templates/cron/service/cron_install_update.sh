#!/bin/sh
CRON_CRONFILE={{ cron_conffile }}
CRON_PROJECTFILE={{ cron_projectfile }}
CRON_PARSESCRIPT={{ deploy_dir }}/service/cron_parse.py

which cron 1>/dev/null || { echo "ERROR: * I require cron but it's not installed."; exit 0; }

if [ -f $CRON_PROJECTFILE ]; then
    sudo python $CRON_PARSESCRIPT
fi
