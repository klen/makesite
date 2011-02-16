#!/bin/sh

# Variables
NGINX_CONFPATH={{ nginx_confpath }}

# Remove link on nginx config
if [ -f $NGINX_CONFPATH ]; then
    echo '  * Remove link to nginx conf:'$NGINX_CONFPATH
    sudo rm -rf $NGINX_CONFPATH
else
    echo '  * Not found template nginx config file: '$NGINX_CONFPATH
fi

# Restart nginx
if [ -f /etc/init.d/nginx ]; then
    echo '  * Restart nginx'
    if [ ! -z "`pgrep nginx`" ]; then
        sudo /etc/init.d/nginx stop
    fi
    sudo /etc/init.d/nginx start
fi
