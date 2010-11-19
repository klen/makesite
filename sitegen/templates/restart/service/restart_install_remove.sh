if [ -f /etc/init.d/nginx ]; then
    echo 'Restart nginx'
    if [ ! -z "$(pgrep nginx)" ]; then
        sudo /etc/init.d/nginx stop
    fi
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    while [ ! -z "$(pgrep supervisord)" ]; do
        echo '  * Stop supervisord'
        sudo /etc/init.d/supervisor stop
        sleep 2
    done
    echo '  * Start supervisord'
    sudo supervisord
fi
