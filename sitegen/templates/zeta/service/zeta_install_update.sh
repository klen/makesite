ZETA_SETTINGS_FILE={{ project_sourcedir }}/.zeta

# Check zeta-library
which zeta 1>/dev/null || { echo "ERROR: * I require zeta but it's not installed."; exit 0; }

if [ -f $ZETA_SETTINGS_FILE ]; then
    STATIC=`cat $ZETA_SETTINGS_FILE`
    for f in $STATIC; do
        zeta $f
    done
fi
