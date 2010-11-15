BRANCH=$!branch!$
PROJECT_NAME=$!project_name!$

SUPERVISOR_PROGRAMM_NAME=$BRANCH.$PROJECT_NAME

echo "Restart supervisor service: $SUPERVISOR_PROGRAMM_NAME."
sudo supervisorctl restart $SUPERVISOR_PROGRAMM_NAME
