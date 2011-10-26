#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd
DEPLOY_DIR={{ deploy_dir }}
SUPERVISOR_CELERY_CONFPATH={{ supervisor_celery_confpath }}

msg_info "Create link to supervisor conf: $SUPERVISOR_CELERY_CONFPATH"
cmd_or_die "sudo ln -sf $DEPLOY_DIR/deploy/supervisor.celeryd.conf $SUPERVISOR_CELERY_CONFPATH"

msg_info "Update supervisord for celeryd"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl reload $PROGRAMM_NAME"
