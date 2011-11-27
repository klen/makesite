#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
BASERUN={{ service_dir }}/virtualenv_run.sh
MEDIA_DIR={{ media_dir }}
DJANGO_SETTINGS={{ django_settings }}

cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"

# Make manage.py executable
[ ! -x $SOURCE_DIR/manage.py ] && {
    echo "Make manage.py executable."
    cmd_or_die "sudo chmod +x $SOURCE_DIR/manage.py"
}

# Django syncdb
CMD="manage.py syncdb --noinput --settings=$DJANGO_SETTINGS 2>/dev/null"
[ -f $BASERUN ] && CMD="$BASERUN $CMD"
cmd "sudo -u $SITE_USER $CMD" || echo "Syncdb skipped"
