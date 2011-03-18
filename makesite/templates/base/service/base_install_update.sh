#!/bin/sh

# Variables
DEPLOY_DIR={{ deploy_dir }}
PROJECT_SERVICEDIR={{ project_servicedir }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}


# Chown deploy dir to config user
sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR

# Make service-files as executable
sudo chmod +x $PROJECT_SERVICEDIR/*.sh
