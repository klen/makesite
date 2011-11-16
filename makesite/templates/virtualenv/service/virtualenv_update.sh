#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
VIRTUALENVDIR={{ virtualenvdir  }}
PIP_PROJECTFILE={{ pip_projectfile }}

REQ_SUM=$(md5sum $PIP_PROJECTFILE)
OLD_REQ_SUM=$(cat $VIRTUALENVDIR/.reqsum)

cmd_or_die "sudo chown -R $USER:$USER $VIRTUALENVDIR"

if [ -f $PIP_PROJECTFILE ]; then
    echo "Update virtualenv requirements: $PIP_PROJECTFILE"
    if [ "$REQ_SUM" = "$OLD_REQ_SUM" ]; then
        echo "Changes not found"
    else
        sudo pip -E $VIRTUALENVDIR install -r $PIP_PROJECTFILE
        cmd_or_die "rm -rf $VIRTUALENVDIR/.reqsum "
        sh -c "md5sum $PIP_PROJECTFILE > $VIRTUALENVDIR/.reqsum"
    fi
fi

# Restore rights
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $VIRTUALENVDIR"
