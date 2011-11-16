#!/bin/bash

. $(dirname $0)/utils.sh

# Copy from source directory to project static directory
cmd_or_die "sudo chown -R $USER:$USER $DEPLOY_DIR"
cmd_or_die "cp -drf $SOURCE_DIR/* $STATIC_DIR/."
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"
