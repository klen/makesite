BRANCH={{ branch }}
PROJECT={{ project }}
SUPERVISOR_PROGRAMM_NAME=$PROJECT.$BRANCH
SUPERVISOR_CONFPATH={{ supervisor_confpath }}

which supervisorctl 1>/dev/null || { echo "ERROR: * I require supervisorctl but it's not installed."; exit 0; }

if [ -f $SUPERVISOR_CONFPATH ]; then
    echo "  * Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
    sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
fi
