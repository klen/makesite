USER={{ user }}
BASERUN={{ deploy_dir }}/service/base_run.sh
DJANGO_SETTINGS={{ django_settings }}

if [ -f $BASERUN ]; then
    echo "  * Run django syncdb."
    sudo -u $USER sh $BASERUN manage.py syncdb --noinput --settings=$DJANGO_SETTINGS
fi

