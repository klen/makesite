BRANCH={{ branch }}
PROJECT={{ project }}
SUPERVISOR_PROGRAMM_NAME=$PROJECT.$BRANCH
SUPERVISOR_CONFPATH={{ supervisor_confpath }}

if ! which supervisorctl >/dev/null; then echo "  * I require supervisorctl but it's not installed."; exit 0; fi

if [ -f $SUPERVISOR_CONFPATH ]; then
    echo "Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
    sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
fi
