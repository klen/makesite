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
cmd_or_die "cd $PROJECT_SOURCEDIR && svn update"
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_SOURCEDIR"
