#!/bin/sh

# Variables
SUPERVISOR_TASKNAME={{ supervisor_taskname }}
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}

# Restart supervisor programm
echo "  * Restart supervisor service: $SUPERVISOR_TASKNAME."
sudo supervisorctl reread
sudo supervisorctl restart $SUPERVISOR_TASKNAME
