GIT_PROJECT_TEMP_DIR=/tmp/{{ project_name }}{{ branch }}
GIT_PROJECT_DIR={{deploy_dir}}/source

git clone {{repo}} $GIT_PROJECT_TEMP_DIR
cd $GIT_PROJECT_TEMP_DIR
git push origin origin:refs/heads/{{branch}}
git fetch origin
git checkout --track origin/{{branch}}

sudo mv $GIT_PROJECT_TEMP_DIR $GIT_PROJECT_DIR
