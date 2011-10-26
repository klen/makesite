#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}
SUPERVISOR_SOURCE_CONFPATH={{ supervisor_source_confpath }}
SUPERVISOR_TASKNAME={{ supervisor_taskname }}

# Add project config to supervisor
cmd_or_die "sudo ln -sf $SUPERVISOR_SOURCE_CONFPATH $SUPERVISOR_TARGET_CONFPATH"

# Restart supervisor
msg_info "Update supervisord"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl reload"
