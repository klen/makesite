#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
SUPERVISOR_TASKNAME={{ supervisor_taskname }}
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}

echo "Restart supervisor service: $SUPERVISOR_TASKNAME"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl restart $SUPERVISOR_TASKNAME"
