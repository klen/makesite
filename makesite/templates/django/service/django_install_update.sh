#!/bin/sh
USER={{ user }}
GROUP={{ group }}
BASERUN={{ deploy_dir }}/service/base_run.sh
STATIC_DIR={{ deploy_dir }}/static
DJANGO_SETTINGS={{ django_settings }}

sudo chown $USER:$GROUP $STATIC_DIR

if [ -f $BASERUN ]; then
    echo "  * Run django migration."
    sudo -u $USER sh $BASERUN manage.py migrate --noinput --settings=$DJANGO_SETTINGS

    echo "  * Run django collect static files."
    sudo -u $USER sh $BASERUN manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS
fi
