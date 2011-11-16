#!/bin/bash

. $(dirname $0)/utils.sh

cmd_or_die "sudo chown $USER:$USER $STATIC_DIR"
olddir=""
for f in `find $STATIC_DIR -name '*.scss'`; do
    dir=`dirname $f`
    if [ ! "$olddir" = "$dir" ]; then
        olddir=$dir
        echo "Compass compile dir: $dir"
        cmd_or_die "compass compile --css-dir=$dir --sass-dir=$dir"
    fi
done

# Restore rights
cmd_or_die "sudo chown -R $SITE_USER:$SITE_GROUP $STATIC_DIR"
