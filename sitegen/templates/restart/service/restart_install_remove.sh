if [ -f /etc/init.d/nginx ]; then
    echo 'Restart nginx'
    if [ ! -z "$(pgrep nginx)" ]; then
        sudo /etc/init.d/nginx stop
    fi
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    echo 'Restart supervisord'
    if [ ! -z "$(pgrep supervisord)" ]; then
        sudo supervisorctl shutdown
        sudo /etc/init.d/supervisor stop
        sleep 2
    fi
    sudo supervisord
fi
