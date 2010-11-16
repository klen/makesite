REPO={{ repo }}
BRANCH={{ branch }}
PROJECT={{ project }}
DEPLOY_DIR={{ deploy_dir }}

GIT_PROJECT_DIR={{ git_project_dir }}
GIT_PROJECT_TEMP_DIR=/tmp/$BRANCH.$PROJECT-$USER

# Check git
type -P git &>/dev/null || { echo "I require git but it's not installed.  Aborting." >&2; exit 1; }

echo "Clone $REPO to $GIT_PROJECT_TEMP_DIR."
rm -rf $GIT_PROJECT_TEMP_DIR
git clone $REPO $GIT_PROJECT_TEMP_DIR

echo "Set branch $BRANCH."
cd $GIT_PROJECT_TEMP_DIR
git push origin origin:refs/heads/$BRANCH
git fetch origin
git checkout --track origin/$BRANCH

echo "Move $GIT_PROJECT_TEMP_DIR to $GIT_PROJECT_DIR"
sudo mv $GIT_PROJECT_TEMP_DIR $GIT_PROJECT_DIR

