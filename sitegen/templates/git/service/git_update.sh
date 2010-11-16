REPO={{ repo }}
BRANCH={{ branch }}
PROJECT={{ project }}
DEPLOY_DIR={{ deploy_dir }}
USER={{ user }}
GROUP={{ group }}

RANDOM_NAME=`</dev/urandom tr -dc A-Za-z0-9 | head -c 8`
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$RANDOM_NAME
GIT_PROJECT_DIR=$DEPLOY_DIR/source

echo "Copy $GIT_PROJECT_DIR to $GIT_PROJECT_TEMP_DIR."
cp -r $GIT_PROJECT_DIR $GIT_PROJECT_TEMP_DIR

cd $GIT_PROJECT_TEMP_DIR && git reset --hard HEAD && git pull
sudo rm -rf $GIT_PROJECT_DIR

echo "Move $GIT_PROJECT_TEMP_DIR to $GIT_PROJECT_DIR"
sudo mv $GIT_PROJECT_TEMP_DIR $GIT_PROJECT_DIR
sudo chown -R $USER:$GROUP $GIT_PROJECT_DIR
