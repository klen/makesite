#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
BRANCH={{ branch }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
GIT_BRANCH_CREATE={{ git_branch_create }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

# Create project branch
if [[ ! "$BRANCH" = "master" ]] && [[ "$GIT_BRANCH_CREATE" = "yes" ]]; then
    cmd "sudo chown -R $USER:$USER $PROJECT_SOURCEDIR"
    cmd "git --work-tree $PROJECT_SOURCEDIR --git-dir $PROJECT_SOURCEDIR/.git push origin origin:refs/heads/$BRANCH"
    cmd "git --work-tree $PROJECT_SOURCEDIR --git-dir $PROJECT_SOURCEDIR/.git fetch origin"
    cmd "git --work-tree $PROJECT_SOURCEDIR --git-dir $PROJECT_SOURCEDIR/.git checkout --track origin/$BRANCH"
    cmd "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR"
fi
