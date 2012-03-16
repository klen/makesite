#!/bin/bash

. $(dirname $0)/utils.sh

VIRTUALENVDIR={{ virtualenvdir }}
PIP_PROJECTFILE={{ pip_projectfile }}
PIP=$VIRTUALENVDIR/bin/pip

# Change rights
sudo chown -R $USER:$USER $DEPLOY_DIR

echo "Create virtualenv: $VIRTUALENVDIR"
cmd_or_die "virtualenv --no-site-packages $VIRTUALENVDIR"

if [ -f $PIP_PROJECTFILE ]; then
    echo "Update virtualenv requirements '$PIP_PROJECTFILE'."
    $PIP install -I -M -r $PIP_PROJECTFILE
    cmd_or_die "rm -rf $VIRTUALENVDIR/.reqsum" 
    sh -c "md5sum $PIP_PROJECTFILE > $VIRTUALENVDIR/.reqsum"
else
    echo "Not found pip requirements file: $PIP_PROJECTFILE"
fi

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR
