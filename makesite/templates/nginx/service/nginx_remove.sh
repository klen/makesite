#!/bin/sh

# Variables
NGINX_TARGET_CONFPATH={{ nginx_target_confpath }}

# Remove link on nginx config
if [ -f $NGINX_TARGET_CONFPATH ]; then
    echo '  * Remove link to nginx conf:'$NGINX_TARGET_CONFPATH
    sudo rm -rf $NGINX_TARGET_CONFPATH
else
    echo '  * Not found template nginx config file: '$NGINX_TARGET_CONFPATH
fi

# Restart nginx
if [ -f /etc/init.d/nginx ]; then
    if [ ! -z "`pgrep nginx`" ]; then
        echo '  * Stop nginx'
        sudo /etc/init.d/nginx stop
    fi
    echo '  * Start nginx'
    sudo /etc/init.d/nginx start
fi
