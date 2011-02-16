#!/bin/sh

# Variables
SITE_USER={{ site_user }}
BASERUN={{ deploy_dir }}/service/base_run.sh
DJANGO_SETTINGS=settings.{{ mode or 'dev' }}

# Migration and collect static
if [ -f $BASERUN ]; then
    echo "  * Run django migration."
    sudo -u $SITE_USER sh $BASERUN manage.py migrate --noinput --settings=$DJANGO_SETTINGS

    echo "  * Run django collect static files."
    sudo -u $SITE_USER sh $BASERUN manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS
fi
