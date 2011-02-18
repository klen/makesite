#!/bin/sh

# Variables
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
DEPLOY_DIR={{ deploy_dir }}
PROJECT_STATICDIR={{ project_staticdir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
SRC={{ src }}
SRC_STATIC_DIR=$PROJECT_SOURCEDIR/static

# Remove project dir
sudo rm -rf $PROJECT_SOURCEDIR

# Copy source directory to project source directory
echo "  * Clone $SRC to $PROJECT_SOURCEDIR."
sudo cp -r $SRC $PROJECT_SOURCEDIR

if [ ! -d $PROJECT_STATICDIR ]; then
    sudo mkdir -p $PROJECT_STATICDIR
fi
# Copy static in static dir
if [ -d $SRC_STATIC_DIR ]; then
    sudo cp -r $SRC_STATIC_DIR/* $PROJECT_STATICDIR
fi

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR
