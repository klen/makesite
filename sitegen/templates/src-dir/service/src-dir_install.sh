SOURCE_DIR={{ sourcedir }}
DEPLOY_DIR={{ deploy_dir }}

echo "  * Clone $SOURCE_DIR to $DEPLOY_DIR"
sudo cp -r $SOURCE_DIR $DEPLOY_DIR/source
