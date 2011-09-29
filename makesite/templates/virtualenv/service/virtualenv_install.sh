#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
DEPLOY_DIR={{ deploy_dir }}
VIRTUALENVDIR={{ virtualenvdir }}
PIP_PROJECTFILE={{ pip_projectfile }}
PYTHON_PREFIX={{ python_prefix }}

# Change rights
cmd "sudo chown -R $USER:$USER $DEPLOY_DIR"

# Check pip and virtualenv
check_program pip
check_program virtualenv

msg_info "Create virtualenv: $VIRTUALENVDIR"
cmd_or_die "virtualenv --no-site-packages $VIRTUALENVDIR"

if [ -f $PIP_PROJECTFILE ]; then
    msg_info "Update virtualenv requirements '$PIP_PROJECTFILE'."
    sudo pip -E $VIRTUALENVDIR install -I -r $PIP_PROJECTFILE
    cmd_or_die "rm -rf $VIRTUALENVDIR/.reqsum" 
    sh -c "md5sum $PIP_PROJECTFILE > $VIRTUALENVDIR/.reqsum"
else
    msg_warning "Not found pip requirements file: $PIP_PROJECTFILE"
fi

# Restore rights
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $DEPLOY_DIR"
