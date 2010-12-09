REPO={{ repo }}
BRANCH={{ branch }}
PROJECT={{ project }}
DEPLOY_DIR={{ deploy_dir }}

PROJECT_SOURCEDIR={{ project_sourcedir }}
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$USER

which git 1>/dev/null || { echo "ERROR: * I require git but it's not installed."; exit 0; }

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

