BASERUN={{ deploy_dir }}/service/base_run.sh
DJANGO_SETTINGS={{ django_settings }}

if [ -f $BASERUN ]; then
    echo "Run django migration."
    sh $BASERUN manage.py migrate --settings=$DJANGO_SETTINGS

    echo "Run django collect static files."
    sh $BASERUN manage.py collectstaticfiles --settings=$DJANGO_SETTINGS
fi
