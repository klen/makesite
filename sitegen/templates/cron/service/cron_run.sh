VIRTUALENVDIR={{ virtualenvdir }}
VIRTUALENVDIR_ACTIVATE=$VIRTUALENVDIR/bin/activate
COMMAND=$@

# Activate virtialenv
if [ -f $VIRTUALENVDIR_ACTIVATE ]; then
    PATH="{{ project_sourcedir }}:$VIRTUALENVDIR/bin:$PATH"
    $COMMAND
fi
