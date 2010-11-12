if [ -f /etc/init.d/nginx ]; then
    /etc/init.d/nginx stop
    /etc/init.d/nginx start
fi

if [ -f /etc/init.d/supervisor ]; then
    /etc/init.d/supervisor stop
    sleep 1
    /etc/init.d/supervisor start
fi
