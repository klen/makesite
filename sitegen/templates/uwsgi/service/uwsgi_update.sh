BRANCH={{ branch }}
PROJECT={{ project }}
SUPERVISOR_PROGRAMM_NAME=$BRANCH.$PROJECT

type -P supervisorctl &>/dev/null || { echo "I require supervisorctl but it's not installed.  Aborting." >&2; exit 1; }

echo "Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
