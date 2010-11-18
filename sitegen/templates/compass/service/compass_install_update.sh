STATIC_DIR={{ deploy_dir }}/static
COMPASSPARAM_IMAGES_DIR=images
COMPASSPARAM_JAVASCRIPT_DIR=javascript
COMPASSPARAM_HTTP_PATH="/"

if ! which compass >/dev/null; then echo "  * I require compass but it's not installed."; exit 0; fi

for d in $STATIC_DIR/*/css; do
    if [ -d $d ]; then
        echo "  * Compass compile dir: '$d'."
        sudo compass compile --css-dir=$d --sass-dir=$d
    fi
done

for d in $STATIC_DIR/*/sass; do
    if [ -d $d ]; then
        echo "  * Compass compile dir: '$d'."
        dirname=$(dirname $d)/css
        sudo compass compile --css-dir=$dirname --sass-dir=$d
    fi
done

sudo chown $USER:$GROUP $STATIC_DIR
sudo find $STATIC_DIR -name "*.scss" -delete
