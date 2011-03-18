#!/bin/sh

# Variables
SITE_USER={{ site_user }}
BASERUN={{ project_servicedir }}/virtualenv_run.sh
PROJECT_SOURCEDIR={{ project_sourcedir }}
MODE={{ mode }}

# Check settings
if [ -d $PROJECT_SOURCEDIR/settings ]; then
    DJANGO_SETTINGS=settings.$MODE
else
    DJANGO_SETTINGS=settings
fi

# Migration and collect static
if [ -f $BASERUN ]; then
    echo "  * Run django migration."
    sudo -u $SITE_USER sh $BASERUN manage.py migrate --noinput --settings=$DJANGO_SETTINGS

    echo "  * Run django collect static files."
    sudo -u $SITE_USER sh $BASERUN manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS
fi
