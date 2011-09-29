#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
CRON_OUTPUTFILE={{ cron_outputfile }}

if [ -f $CRON_OUTPUTFILE ]; then
    msg_info "Remove cron file: $CRON_OUTPUTFILE"
    cmd_or_die "sudo rm -rf $CRON_OUTPUTFILE"
fi
