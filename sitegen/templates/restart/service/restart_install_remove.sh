if [ -f /etc/init.d/nginx ]; then
    echo 'Restart nginx'
    sudo /etc/init.d/nginx stop
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    echo 'Restart supervisord'
    sudo supervisorctl shutdown
    sudo supervisord
fi
