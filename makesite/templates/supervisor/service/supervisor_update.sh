#!/bin/sh

# Variables
SUPERVISOR_PROGRAMM_NAME={{ project }}.{{ branch }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}

# Restart supervisor programm
if [ -f $SUPERVISOR_CONFPATH ]; then
    echo "  * Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
    sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
fi
