#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
SRC_STATIC_DIR=$SOURCE_DIR/static

# Remove project dir
cmd "sudo rm -rf $SOURCE_DIR"

# Copy source directory to project source directory
echo "Clone $SRC to $SOURCE_DIR"
cmd "sudo cp -r $SRC $SOURCE_DIR"

cmd "mkdir -p $STATIC_DIR"
if [ -d $SRC_STATIC_DIR ]; then
    cmd "sudo cp -r $SRC_STATIC_DIR/* $STATIC_DIR"
fi

# Restore rights
cmd "sudo chown -R $SITE_USER:$SITE_GROUP $STATIC_DIR"
cmd "sudo chown -R $SITE_USER:$SITE_GROUP $SOURCE_DIR"
