#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SRC={{ src }}
DEPLOY_DIR={{ deploy_dir }}
SRC_STATIC_DIR={{ project_sourcedir }}/static
PROJECT_STATICDIR={{ project_staticdir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

# Change rights
cmd_or_die "sudo chown -R $USER:$USER $DEPLOY_DIR"

# Copy source directory to project source directory
cmd_or_die "cp -r $SRC $PROJECT_SOURCEDIR"

# Copy static in static dir
if [ -d $SRC_STATIC_DIR ]; then
    cmd_or_die "cp -r $SRC_STATIC_DIR/* $PROJECT_STATICDIR"
fi
