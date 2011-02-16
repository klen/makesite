#!/bin/sh

# Variables
BRANCH={{ branch }}
PROJECT={{ project }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
GIT_PROJECT_TEMP_DIR="/tmp/$BRANCH.$PROJECT-$SITE_USER"


echo "  * Copy $PROJECT_SOURCEDIR to $GIT_PROJECT_TEMP_DIR."
rm -rf $GIT_PROJECT_TEMP_DIR
cp -r $PROJECT_SOURCEDIR $GIT_PROJECT_TEMP_DIR

cd $GIT_PROJECT_TEMP_DIR && git reset --hard HEAD && git clean -df && git pull

echo "  * Move $GIT_PROJECT_TEMP_DIR to $PROJECT_SOURCEDIR"
sudo rm -rf $PROJECT_SOURCEDIR
sudo mv $GIT_PROJECT_TEMP_DIR $PROJECT_SOURCEDIR

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR
