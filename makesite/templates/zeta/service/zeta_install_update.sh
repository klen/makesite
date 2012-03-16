#!/bin/bash

. $(dirname $0)/utils.sh

# Change rights
cmd_or_die "sudo chown -R $USER:$USER $STATIC_DIR"

# Pack static
cmd_or_die "zeta -p _ $STATIC_DIR"

# Restore rights
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $STATIC_DIR"
