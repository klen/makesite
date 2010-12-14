REPO={{ repo }}
BRANCH={{ branch }}
PROJECT={{ project }}
DEPLOY_DIR={{ deploy_dir }}

PROJECT_SOURCEDIR={{ project_sourcedir }}
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$USER

which git 1>/dev/null || {
        echo -e "  * Git not found! Attempting to install..."
        if [ -f /etc/lsb-release ] ; then
                sudo apt-get install git
        elif [ -f /etc/fedora-release ] ; then
                sudo yum install git
        elif [ -f /etc/debian_version ] ; then
                sudo apt-get install git
        fi
}

echo "  * Clone $REPO to $GIT_PROJECT_TEMP_DIR."
rm -rf $GIT_PROJECT_TEMP_DIR
git clone $REPO $GIT_PROJECT_TEMP_DIR

echo "  * Set branch $BRANCH."
cd $GIT_PROJECT_TEMP_DIR
git push origin origin:refs/heads/$BRANCH
git fetch origin
git checkout --track origin/$BRANCH

echo "  * Move $GIT_PROJECT_TEMP_DIR to $PROJECT_SOURCEDIR"
sudo mv $GIT_PROJECT_TEMP_DIR $PROJECT_SOURCEDIR

