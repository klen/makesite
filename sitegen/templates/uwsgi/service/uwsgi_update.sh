BRANCH={{ branch }}
PROJECT={{ project }}
SUPERVISOR_PROGRAMM_NAME=$BRANCH.$PROJECT

if ! which supervisorctl >/dev/null; then echo "  * I require supervisorctl but it's not installed."; exit 0; fi

echo "Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
