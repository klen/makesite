#!/bin/sh

NGINX_CONFPATH={{ nginx_confpath }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}

if [ -f $NGINX_CONFPATH ]; then
    echo '  * Remove link to nginx conf:'$NGINX_CONFPATH
    sudo rm -rf $NGINX_CONFPATH
fi

if [ -f $SUPERVISOR_CONFPATH ]; then
    echo '  * Remove link to supervisor conf:'$SUPERVISOR_CONFPATH
    sudo rm -rf $SUPERVISOR_CONFPATH
fi
