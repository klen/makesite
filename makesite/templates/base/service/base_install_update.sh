#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
DEPLOY_DIR={{ deploy_dir }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}

# Check sudo
check_program sudo

# Chown deploy dir to config user
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"
