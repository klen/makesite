#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
NGINX_SOURCE_CONFPATH={{ nginx_source_confpath }}
NGINX_TARGET_CONFPATH={{ nginx_target_confpath }}

# Add site to nginx enabled sites
echo "Create link to nginx conf: $NGINX_TARGET_CONFPATH"
cmd_or_die "sudo ln -sf $NGINX_SOURCE_CONFPATH $NGINX_TARGET_CONFPATH"

# Reload nginx
if [ -f /etc/init.d/nginx ]; then
    cmd_or_die "sudo /etc/init.d/nginx reload"
fi
