#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}
SUPERVISOR_TASKNAME={{ supervisor_taskname }}

# Remove link on supervisor config
cmd_or_die "sudo rm -f $SUPERVISOR_TARGET_CONFPATH"

# Restart supervisor
msg_info "Update supervisord"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl reload"
