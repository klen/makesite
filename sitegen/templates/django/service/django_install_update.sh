USER={{ user }}
GROUP={{ group }}
BASERUN={{ deploy_dir }}/service/base_run.sh
STATIC_DIR={{ deploy_dir }}/static
DJANGO_SETTINGS={{ django_settings }}

if [ -f $BASERUN ]; then
    echo "Run django migration."
    sudo -u $USER sh $BASERUN manage.py migrate --settings=$DJANGO_SETTINGS

    echo "Run django collect static files."
    sudo chown $USER:$GROUP $STATIC_DIR
    sudo -u $USER sh $BASERUN manage.py collectstatic --settings=$DJANGO_SETTINGS
fi
