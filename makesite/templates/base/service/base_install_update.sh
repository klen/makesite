#!/bin/sh

DEPLOY_DIR={{ deploy_dir }}
PROJECT_SERVICEDIR={{ project_servicedir }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}

# Make rights
sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR

# Make exetable service files
sudo chmod +x $PROJECT_SERVICEDIR/*.sh
