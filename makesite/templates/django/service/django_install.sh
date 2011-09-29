#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
BASERUN={{ project_servicedir }}/virtualenv_run.sh
MEDIA_DIR={{ media_dir }}
MODE={{ mode }}

# Check settings
if [ -d $PROJECT_SOURCEDIR/settings ]; then
    DJANGO_SETTINGS=settings.$MODE
else
    DJANGO_SETTINGS=settings
fi

# Create manage.py executable
if [ ! -x $PROJECT_SOURCEDIR/manage.py ]; then
    msg_info "Make manage.py executable."
    cmd_or_die "sudo chmod +x $PROJECT_SOURCEDIR/manage.py"
fi

# Sync database
if [ -f $BASERUN ]; then
    msg_info "Run django syncdb"
    cmd_or_die "$BASERUN manage.py syncdb --noinput --settings=$DJANGO_SETTINGS"
fi
