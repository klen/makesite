#!/bin/bash

. $(dirname $0)/utils.sh

# Chown deploy dir to config user
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"
