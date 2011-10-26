#!/bin/bash

# Import BSFL
source {{ project_servicedir }}/.bsfl

# Variables
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_STATICDIR={{ project_staticdir }}

# Change rights
cmd_or_die "sudo chown -R $USER:$USER $PROJECT_STATICDIR"

# Pack static
cmd_or_die "zeta $PROJECT_STATICDIR"

# Restore rights
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR"
