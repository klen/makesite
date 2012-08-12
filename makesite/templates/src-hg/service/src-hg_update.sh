#!/bin/bash

. $(dirname $0)/utils.sh

cmd_or_die "sudo chown -R $USER:$USER $SOURCE_DIR"
cmd_or_die "sudo -u $SRC_USER cd $SOURCE_DIR && hg update -C && hg pull"
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $SOURCE_DIR"
