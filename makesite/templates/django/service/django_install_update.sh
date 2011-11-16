#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
BASERUN={{ service_dir }}/virtualenv_run.sh

# Check settings
if [ -d $SOURCE_DIR/settings ]; then
    DJANGO_SETTINGS=settings.$MODE
else
    DJANGO_SETTINGS=settings
fi

# Migration and collect static
if [ -f $BASERUN ]; then
    echo "Run django migration"
    cmd_or_die "sudo -u $SITE_USER sh $BASERUN manage.py migrate --noinput --settings=$DJANGO_SETTINGS"

    echo "Run django collect static files"
    cmd_or_die "sudo -u $SITE_USER sh $BASERUN manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS"
fi
