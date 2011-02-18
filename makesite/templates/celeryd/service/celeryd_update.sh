#!/bin/sh

# Variables
SUPERVISOR_PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd
SUPERVISOR_CONFPATH={{ supervisor_confpath }}.celeryd.conf

# Restart supervisor programm
if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord for celeryd'
    sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
fi
