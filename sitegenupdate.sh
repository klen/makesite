#!/bin/sh

if [ $# -ne 3 ]; then
    echo "Usage: sitegenupdate SITES_HOME PROJECT BRANCH"
    exit 0
fi

SITES_HOME=$1
PROJECT_DIR=$SITES_HOME/$2/$3
SERVICE_DIR=$PROJECT_DIR/service

_verify_sites_home () {
    if [ ! -d $SITES_HOME ]; then
        echo "Error: sites home dir '$SITES_HOME' not found."
        return 0
    fi
}

_verify_project_dir () {
    if [ ! -d $PROJECT_DIR ]; then
        echo "Error: project dir '$PROJECT_DIR' not found."
        return 0
    fi
}

_update () {
    echo "Update project '$PROJECT_DIR'."
    cd $SERVICE_DIR
    for f in *_update.sh
    do
        echo "Run '$f'"
        sh $f
    done
}


_verify_sites_home || return 1
_verify_project_dir || return 1
_update

