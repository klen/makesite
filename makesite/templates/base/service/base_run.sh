VIRTUALENVDIR={{ virtualenvdir }}
VIRTUALENVDIR_ACTIVATE=$VIRTUALENVDIR/bin/activate
COMMAND=$@

PATH="{{ project_sourcedir }}:$PATH"

if [ -f $VIRTUALENVDIR_ACTIVATE ]; then
    PATH="$VIRTUALENVDIR/bin:$PATH"
fi

export PATH
$COMMAND
