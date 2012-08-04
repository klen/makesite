#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
PROGRAMM_NAME=$PROJECT.$SAFE_BRANCH.celery

# Restart supervisor programm
echo "Update supervisord for celeryd"
cmd_or_die "sudo supervisorctl restart $PROGRAMM_NAME"
