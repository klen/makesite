#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
DEPLOY_DIR={{ deploy_dir }}
PROJECT_STATICDIR={{ project_staticdir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
SRC={{ src }}
SRC_STATIC_DIR=$PROJECT_SOURCEDIR/static

# Remove project dir
cmd "sudo rm -rf $PROJECT_SOURCEDIR"

# Copy source directory to project source directory
msg_info "Clone $SRC to $PROJECT_SOURCEDIR"
cmd "sudo cp -r $SRC $PROJECT_SOURCEDIR"

cmd "mkdir -p $PROJECT_STATICDIR"
if [ -d $SRC_STATIC_DIR ]; then
    cmd "sudo cp -r $SRC_STATIC_DIR/* $PROJECT_STATICDIR"
fi

# Restore rights
cmd "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR"
cmd "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR"
