PROGRAMM_NAME={{ project }}.{{ branch }}

if [ -f /etc/init.d/nginx ]; then
    echo 'Restart nginx'
    if [ ! -z "`pgrep nginx`" ]; then
        sudo /etc/init.d/nginx stop
    fi
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    echo 'Update supervisord'
    sudo supervisorctl reread
    sudo supervisorctl reload $PROGRAMM_NAME
fi
