#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
BASERUN={{ service_dir }}/virtualenv_run.sh
DJANGO_SETTINGS={{ django_settings }}

cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"

# Django migration
CMD="manage.py migrate --noinput --settings=$DJANGO_SETTINGS 2>/dev/null"
[ -f $BASERUN ] && CMD="$BASERUN $CMD"
cmd "sudo -u $SITE_USER $CMD" || echo "Migration skipped"

# Django collectstatic
CMD="manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS 2>/dev/null"
[ -f $BASERUN ] && CMD="$BASERUN $CMD"
cmd "sudo -u $SITE_USER $CMD" || echo "Collect static skipped"
