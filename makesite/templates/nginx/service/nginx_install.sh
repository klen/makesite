#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
NGINX_SOURCE_CONFPATH={{ nginx_source_confpath }}
NGINX_TARGET_CONFPATH={{ nginx_target_confpath }}

# Check nginx
check_program nginx

# Add site to nginx enabled sites
msg_info "Create link to nginx conf: $NGINX_TARGET_CONFPATH"
cmd_or_die "sudo ln -sf $NGINX_SOURCE_CONFPATH $NGINX_TARGET_CONFPATH"

# Reload nginx
if [ -f /etc/init.d/nginx ]; then
    cmd_or_die "sudo /etc/init.d/nginx reload"
fi
