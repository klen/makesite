#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
NGINX_TARGET_CONFPATH={{ nginx_target_confpath }}

cmd_or_die "sudo rm -rf $NGINX_TARGET_CONFPATH"

# Restart nginx
if [ -f /etc/init.d/nginx ]; then
    cmd_or_die "sudo /etc/init.d/nginx restart"
fi
