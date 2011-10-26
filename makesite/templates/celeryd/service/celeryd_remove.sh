#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd
SUPERVISOR_CELERY_CONFPATH={{ supervisor_celery_confpath }}

if [ -f $SUPERVISOR_CELERY_CONFPATH ]; then
    msg_info "Remove link to celeryd supervisor conf: $SUPERVISOR_CELERY_CONFPATH"
    cmd_or_die "sudo rm -rf $SUPERVISOR_CELERY_CONFPATH"
fi

msg_info "Update supervisord for celeryd"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl reload"
