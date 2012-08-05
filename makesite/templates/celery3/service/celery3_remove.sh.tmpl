#!/bin/bash

source $(dirname $0)/utils.sh

PROGRAMM_NAME=$PROJECT.$SAFE_BRANCH.celery
CELERY_CONFPATH={{ celery_svconf }}

if [ -f $CELERY_CONFPATH ]; then
    echo "Remove link to celeryd supervisor conf: $CELERY_CONFPATH"
    cmd_or_die "sudo rm -rf $CELERY_CONFPATH"
fi

echo "Update supervisord for celeryd"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl reload"
