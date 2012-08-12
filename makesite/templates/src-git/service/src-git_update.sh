#!/bin/bash

. $(dirname $0)/utils.sh

cmd_or_die "sudo chown -R $SRC_USER:$SRC_USER $SOURCE_DIR"
cd $SOURCE_DIR
cmd_or_die "sudo -u $SRC_USER git reset --hard HEAD"
cmd_or_die "sudo -u $SRC_USER git clean -df"
cmd_or_die "sudo -u $SRC_USER git pull"
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $SOURCE_DIR"
