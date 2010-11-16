SUPERVISORD=/usr/local/bin/supervisord
SUPERVISORCTL=/usr/local/bin/supervisorctl

if [ -f /etc/init.d/nginx ]; then
    echo "Restart nginx"
    sudo /etc/init.d/nginx stop
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    echo "Restart supervisor"
    $SUPERVISORCTL shutdown
    $SUPERVISORD
fi
