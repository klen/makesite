#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
BRANCH={{ branch }}
PROJECT={{ project }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

cmd_or_die "sudo chown -R $USER:$USER $PROJECT_SOURCEDIR"
cmd "cd $PROJECT_SOURCEDIR"
cmd "git reset --hard HEAD"
cmd "git clean -df"
cmd "git pull origin $BRANCH"
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR"
