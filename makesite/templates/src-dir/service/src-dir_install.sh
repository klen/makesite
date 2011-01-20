#!/bin/sh
USER={{ user }}
GROUP={{ group }}
STATIC_DIR={{ project_staticdir }}
SOURCE_DIR={{ project_sourcedir }}
SRC_DIR={{ sourcedir }}
SRC_STATIC_DIR={{ deploy_dir }}/source/static

echo "  * Clone $SRC_DIR to $SOURCE_DIR."
sudo cp -r $SRC_DIR $SOURCE_DIR

# Copy static in static dir
if [ -d $SRC_STATIC_DIR ]; then
    sudo cp -r $SRC_STATIC_DIR/* $STATIC_DIR
fi

sudo chown $USER:$GROUP $STATIC_DIR
sudo chown $USER:$GROUP $SOURCE_DIR
