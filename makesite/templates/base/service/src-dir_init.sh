#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SRC={{ src }}
DEPLOY_DIR={{ deploy_dir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

# Change rights
cmd_or_die "sudo chown -R $USER:$USER $DEPLOY_DIR"

# Copy source directory to project source directory
cmd_or_die "cp -rf $SRC $PROJECT_SOURCEDIR"
