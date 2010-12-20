SOURCE_DIR={{ sourcedir }}
DEPLOY_DIR={{ deploy_dir }}

echo "  * Clone $SOURCE_DIR to $DEPLOY_DIR"
sudo cp -r $SOURCE_DIR $DEPLOY_DIR/source

# Copy static in static dir
if [ -d $DEPLOY_DIR/source/static ]; then
    sudo cp -r $DEPLOY_DIR/source/static/* $DEPLOY_DIR/static
fi
