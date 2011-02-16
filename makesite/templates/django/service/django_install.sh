#!/bin/sh

# Variables
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
BASERUN={{ deploy_dir }}/service/base_run.sh
MODE={{ mode }}

# Check settings
if [ -d $PROJECT_SOURCEDIR/settings ]; then
    DJANGO_SETTINGS=settings.$MODE
else
    DJANGO_SETTINGS=settings
fi

# Create manage.py executable
if [ ! -x $PROJECT_SOURCEDIR/manage.py ]; then
    sudo chmod +x $PROJECT_SOURCEDIR/manage.py
fi

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR

# Sync database
if [ -f $BASERUN ]; then
    echo "  * Run django syncdb."
    sudo -u $SITE_USER sh $BASERUN manage.py syncdb --noinput --settings=$DJANGO_SETTINGS
fi
