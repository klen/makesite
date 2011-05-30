#!/bin/sh

# Variables
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}
SUPERVISOR_TASKNAME={{ supervisor taskname }}

# Remove link on supervisor config
sudo rm $SUPERVISOR_TARGET_CONFPATH || echo '  * Not found template nginx config file: '$SUPERVISOR_TARGET_CONFPATH

# Restart supervisor
if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord'
    sudo supervisorctl reread
    sudo supervisorctl reload
fi
