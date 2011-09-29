#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SUPERVISOR_TASKNAME={{ supervisor_taskname }}
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}

msg_info "Restart supervisor service: $SUPERVISOR_TASKNAME"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl restart $SUPERVISOR_TASKNAME"
