#!/bin/sh

# Variables
SUPERVISOR_CONFPATH={{ supervisor_confpath }}
PROGRAMM_NAME={{ project }}.{{ branch }}

# Remove link on nginx config
if [ -f $SUPERVISOR_CONFPATH ]; then
    echo '  * Remove link to nginx conf:'$SUPERVISOR_CONFPATH
    sudo rm -rf $SUPERVISOR_CONFPATH
else
    echo '  * Not found template nginx config file: '$SUPERVISOR_CONFPATH
fi

# Restart supervisor
if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord'
    sudo supervisorctl reread
    sudo supervisorctl reload $PROGRAMM_NAME
fi
