#!/bin/sh

# Variables
SRC={{ src }}
BRANCH={{ branch }}
PROJECT={{ project }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$USER


# Check git installed.
which git 1>/dev/null || {
    echo "  * Git not found! Attempting to install..."
    if [ -f /etc/lsb-release ] ; then
        sudo apt-get install git
    elif [ -f /etc/fedora-release ] ; then
        sudo yum install git
    elif [ -f /etc/debian_version ] ; then
        sudo apt-get install git
    fi
}

# Clone git repo
echo "  * Clone $SRC to $GIT_PROJECT_TEMP_DIR."
rm -rf $GIT_PROJECT_TEMP_DIR
git clone $SRC $GIT_PROJECT_TEMP_DIR

# Create project branch
echo "  * Set branch $BRANCH."
cd $GIT_PROJECT_TEMP_DIR
git push origin origin:refs/heads/$BRANCH
git fetch origin
git checkout --track origin/$BRANCH

echo "  * Move $GIT_PROJECT_TEMP_DIR to $PROJECT_SOURCEDIR"
sudo mv $GIT_PROJECT_TEMP_DIR $PROJECT_SOURCEDIR

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR
