#!/bin/sh

# Variables
VIRTUALENVDIR={{ virtualenvdir }}
VIRTUALENVDIR_ACTIVATE=$VIRTUALENVDIR/bin/activate
PROJECT_SOURCEDIR={{ project_sourcedir }}
COMMAND=$@


# Add project sourcedir to path
PATH="$PROJECT_SOURCEDIR:$PATH"

# Enable virtualenv if it exists
if [ -f $VIRTUALENVDIR_ACTIVATE ]; then
    PATH="$VIRTUALENVDIR/bin:$PATH"
fi

# Run custom command
export PATH
cd $PROJECT_SOURCEDIR
$COMMAND
