#!/bin/sh

SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
DEPLOY_DIR={{ deploy_dir }}
PROJECT_STATICDIR={{ project_staticdir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
SRC_DIR={{ sourcedir }}
SRC_STATIC_DIR={{ deploy_dir }}/source/static

echo "  * Clone $SRC_DIR to $PROJECT_SOURCEDIR."
sudo cp -r $SRC_DIR $PROJECT_SOURCEDIR

# Copy static in static dir
if [ -d $SRC_STATIC_DIR ]; then
    sudo cp -r $SRC_STATIC_DIR/* $PROJECT_STATICDIR
fi

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR
