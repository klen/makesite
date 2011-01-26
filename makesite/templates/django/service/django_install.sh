#!/bin/sh

SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
BASERUN={{ deploy_dir }}/service/base_run.sh
DJANGO_SETTINGS={{ django_settings }}

sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR

if [ -f $BASERUN ]; then
    echo "  * Run django syncdb."
    sudo -u $SITE_USER sh $BASERUN manage.py syncdb --noinput --settings=$DJANGO_SETTINGS
fi
