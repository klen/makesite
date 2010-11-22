STATIC_DIR={{ deploy_dir }}/static

if ! which compass >/dev/null; then echo "  * I require compass but it's not installed."; exit 0; fi

olddir=""
for f in $(find $STATIC_DIR -name '*.scss'); do
    dir=$(dirname $f)
    if [ ! "$olddir" = "$dir" ]; then
        olddir=$dir
        echo "  * Compass compile dir: '$dir'"
        sudo compass compile --css-dir=$dir --sass-dir=$dir
    fi
done

sudo chown $USER:$GROUP $STATIC_DIR
sudo find $STATIC_DIR -name "*.scss" -delete
sudo find $STATIC_DIR -name "*.rb" -delete
