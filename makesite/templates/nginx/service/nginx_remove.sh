#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
NGINX_TARGET_CONFPATH={{ nginx_target_confpath }}

cmd_or_die "sudo rm -rf $NGINX_TARGET_CONFPATH"

# Restart nginx
if [ -f /etc/init.d/nginx ]; then
    cmd_or_die "sudo /etc/init.d/nginx restart"
fi
