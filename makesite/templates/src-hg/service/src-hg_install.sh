#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
BRANCH={{ branch }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
HG_BRANCH_CREATE={{ hg_branch_create }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

# Create project branch
if [[ ! "$BRANCH" = "master" ]] && [[ "$HG_BRANCH_CREATE" = "yes" ]]; then
    cmd_or_die "sudo chown -R $USER:$USER $PROJECT_SOURCEDIR"
    cmd "hg branch $BRANCH && hg commit && hg push"
    cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR"
fi
