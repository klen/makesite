if [ -f /etc/init.d/nginx ]; then
    echo 'Restart nginx'
    if [ ! -z "`pgrep nginx`" ]; then
        sudo /etc/init.d/nginx stop
    fi
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    echo 'Restart supervisord'
    while [ ! -z "`pgrep supervisord`" ]; do
        sudo /etc/init.d/supervisor stop
        sleep 2
    done
    sudo supervisord
fi
