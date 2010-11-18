STATIC_DIR=/sites/intranet/twimonitor/static
COMPASSPARAM_IMAGES_DIR=images
COMPASSPARAM_JAVASCRIPT_DIR=javascript
COMPASSPARAM_HTTP_PATH="/"

if ! which compass >/dev/null; then echo "  * I require compass but it's not installed."; exit 0; fi

olddir=""
for f in $(find $STATIC_DIR -name '*.scss'); do
    dir=$(dirname $f)
    if [ ! "$olddir" = "$dir" ]; then
        olddir=$dir
        echo "  * Compass compile dir: '%s'" % $dir
        sudo compass compile --css-dir=$dir --sass-dir=$dir
    fi
done

sudo chown $USER:$GROUP $STATIC_DIR
sudo find $STATIC_DIR -name "*.scss" -delete
sudo find $STATIC_DIR -name "*.rb" -delete
