#!/bin/bash

. $(dirname $0)/utils.sh

cmd_or_die "sudo chown -R $USER:$USER $SOURCE_DIR"
cmd_or_die "cd $SOURCE_DIR && svn update"
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $SOURCE_DIR"
