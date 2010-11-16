DEPLOY_DIR={{ deploy_dir }}

echo "Update virtualenv requirements '$DEPLOY_DIR/source/requirements.txt'."
sudo pip -E $DEPLOY_DIR/.virtualenv install -r $DEPLOY_DIR/source/requirements.txt
