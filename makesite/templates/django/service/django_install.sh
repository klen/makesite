#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
BASERUN={{ service_dir }}/virtualenv_run.sh
MEDIA_DIR={{ media_dir }}

# Check settings
if [ -d $SOURCE_DIR/settings ]; then
    DJANGO_SETTINGS=settings.$MODE
else
    DJANGO_SETTINGS=settings
fi

cmd_or_die "sudo chown -R $USER:$USER $SOURCE_DIR"

# Create manage.py executable
if [ ! -x $SOURCE_DIR/manage.py ]; then
    echo "Make manage.py executable."
    cmd_or_die "sudo chmod +x $SOURCE_DIR/manage.py"
fi

# Sync database
if [ -f $BASERUN ]; then
    echo "Run django syncdb"
    cmd_or_die "$BASERUN manage.py syncdb --noinput --settings=$DJANGO_SETTINGS"
fi

cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $SOURCE_DIR"
