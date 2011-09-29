#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SUPERVISOR_PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd

check_program supervisorctl

# Restart supervisor programm
msg_info "Update supervisord for celeryd"
cmd_or_die "sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME"
