STATIC_DIR={{ project_staticdir }}
USER={{ user }}
GROUP={{ group }}

which compass 1>/dev/null || { echo "ERROR: * I require compass but it's not installed."; exit 0; }

olddir=""
for f in `find $STATIC_DIR -name '*.scss'`; do
    dir=`dirname $f`
    if [ ! "$olddir" = "$dir" ]; then
        olddir=$dir
        echo "  * Compass compile dir: '$dir'"
        sudo compass compile --css-dir=$dir --sass-dir=$dir
    fi
done

echo "  * Drop sass files from static."
sudo chown $USER:$GROUP $STATIC_DIR
sudo find $STATIC_DIR -name "*.scss" -delete
sudo find $STATIC_DIR -name "*.rb" -delete
