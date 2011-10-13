#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
DEPLOY_DIR={{ deploy_dir }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
PROJECT_STATICDIR={{ project_staticdir }}

# Copy from source directory to project static directory
cmd_or_die "sudo chown -R $USER:$USER $DEPLOY_DIR"
cmd_or_die "cp -drf $PROJECT_SOURCEDIR/* $PROJECT_STATICDIR/."
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"
