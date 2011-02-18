#!/bin/sh

# Variables
PROJECT_STATICDIR={{ project_staticdir }}
SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}

# Check compass
which compass 1>/dev/null || { echo "ERROR: * I require compass but it's not installed."; exit 0; }

olddir=""
for f in `find $PROJECT_STATICDIR -name '*.scss'`; do
    dir=`dirname $f`
    if [ ! "$olddir" = "$dir" ]; then
        olddir=$dir
        echo "  * Compass compile dir: '$dir'"
        sudo compass compile --css-dir=$dir --sass-dir=$dir
    fi
done

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR

echo "  * Drop sass files from static."
sudo find $PROJECT_STATICDIR -name "*.scss" -delete
sudo find $PROJECT_STATICDIR -name "*.rb" -delete
