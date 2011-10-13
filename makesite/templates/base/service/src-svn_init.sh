#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
SRC={{ src }}
BRANCH={{ branch }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
DEPLOY_DIR={{ deploy_dir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

# Change rights
cmd_or_die "sudo chown -R $USER:$USER $DEPLOY_DIR"

# Check subversion installed.
check_program svn

# Clone mercurial repo
cmd "svn checkout $SRC $PROJECT_SOURCEDIR"
