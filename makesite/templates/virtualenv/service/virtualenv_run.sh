#!/bin/sh

# Variables
VIRTUALENVDIR={{ virtualenvdir }}
PROJECT_SOURCEDIR={{ project_sourcedir }}

COMMAND=$@

# Modify path
PATH="$VIRTUALENVDIR/bin:$PROJECT_SOURCEDIR:$PATH"

# Run custom command
export PATH
cd $PROJECT_SOURCEDIR
$COMMAND
