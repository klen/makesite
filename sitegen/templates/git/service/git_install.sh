REPO={{ repo }}
BRANCH={{ branch }}
PROJECT={{ project }}
DEPLOY_DIR={{ deploy_dir }}

RANDOM_NAME=`</dev/urandom tr -dc A-Za-z0-9 | head -c 8`
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$RANDOM_NAME
GIT_PROJECT_DIR=$DEPLOY_DIR/source

echo "Clone $REPO to $GIT_PROJECT_TEMP_DIR."
git clone $REPO $GIT_PROJECT_TEMP_DIR

echo "Set branch $BRANCH."
cd $GIT_PROJECT_TEMP_DIR

git push origin origin:refs/heads/$BRANCH
git fetch origin
git checkout --track origin/$BRANCH

echo "Move $GIT_PROJECT_TEMP_DIR to $GIT_PROJECT_DIR"
sudo mv $GIT_PROJECT_TEMP_DIR $GIT_PROJECT_DIR
