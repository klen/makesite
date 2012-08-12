#!/bin/bash

. $(dirname $0)/utils.sh

cmd_or_die "sudo chown -R $SRC_USER:$SRC_USER $SOURCE_DIR"
cd $SOURCE_DIR
cmd_or_die "sudo -u $SRC_USER hg update -C"
cmd_or_die "sudo -u $SRC_USER hg pull"
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $SOURCE_DIR"
