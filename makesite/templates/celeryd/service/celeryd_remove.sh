PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd
SUPERVISOR_CONFPATH={{ supervisor_confpath }}.celeryd.conf

if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord for celeryd'
    sudo supervisorctl stop $PROGRAMM_NAME
fi

if [ -f $SUPERVISOR_CONFPATH ]; then
    echo '  * Remove link to celeryd supervisor conf:'$SUPERVISOR_CONFPATH
    sudo rm -rf $SUPERVISOR_CONFPATH
fi

if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord for celeryd'
    sudo supervisorctl reread
fi
