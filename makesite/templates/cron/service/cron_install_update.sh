#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
CRON_PROJECTFILE={{ cron_projectfile }}
CRON_PARSESCRIPT={{ deploy_dir }}/service/cron_parse.py


# Check cron installed.
check_program cron

if [ -f $CRON_PROJECTFILE ]; then
    cmd_or_die "sudo python $CRON_PARSESCRIPT"
fi
