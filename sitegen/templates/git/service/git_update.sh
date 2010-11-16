BRANCH={{ branch }}
PROJECT={{ project }}
GIT_USER={{ user }}
GIT_GROUP={{ group }}

GIT_PROJECT_DIR={{ git_project_dir }}
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$USER

# Check git
type -P git &>/dev/null || { echo "I require git but it's not installed.  Aborting." >&2; exit 1; }

echo "Copy $GIT_PROJECT_DIR to $GIT_PROJECT_TEMP_DIR."
rm -rf $GIT_PROJECT_TEMP_DIR
cp -r $GIT_PROJECT_DIR $GIT_PROJECT_TEMP_DIR

cd $GIT_PROJECT_TEMP_DIR && git reset --hard HEAD && git pull

echo "Move $GIT_PROJECT_TEMP_DIR to $GIT_PROJECT_DIR"
sudo rm -rf $GIT_PROJECT_DIR
sudo mv $GIT_PROJECT_TEMP_DIR $GIT_PROJECT_DIR
sudo chown -R $GIT_USER:$GIT_GROUP $GIT_PROJECT_DIR

