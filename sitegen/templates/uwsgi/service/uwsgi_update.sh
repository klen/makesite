BRANCH={{ branch }}
PROJECT={{ project }}

SUPERVISOR_PROGRAMM_NAME=$BRANCH.$PROJECT

echo "Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
