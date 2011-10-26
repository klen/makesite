#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
PROJECT_STATICDIR={{ project_staticdir }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}

cmd_or_die "sudo chown $USER:$USER $PROJECT_STATICDIR"

olddir=""
for f in `find $PROJECT_STATICDIR -name '*.scss'`; do
    dir=`dirname $f`
    if [ ! "$olddir" = "$dir" ]; then
        olddir=$dir
        msg_info "Compass compile dir: $dir"
        cmd_or_die "compass compile --css-dir=$dir --sass-dir=$dir"
    fi
done

# Restore rights
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR"
