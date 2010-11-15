if [ -f /etc/init.d/nginx ]; then
    sudo /etc/init.d/nginx stop
    sudo /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    sudo /etc/init.d/supervisor stop
    sleep 2
    sudo /etc/init.d/supervisor start
fi
