#!/bin/bash

. $(dirname $0)/utils.sh

PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd
SUPERVISOR_CELERY_CONFPATH={{ supervisor_celery_confpath }}

if [ -f $SUPERVISOR_CELERY_CONFPATH ]; then
    echo "Remove link to celeryd supervisor conf: $SUPERVISOR_CELERY_CONFPATH"
    cmd_or_die "sudo rm -rf $SUPERVISOR_CELERY_CONFPATH"
fi

echo "Update supervisord for celeryd"
cmd_or_die "sudo supervisorctl reread"
cmd_or_die "sudo supervisorctl reload"
