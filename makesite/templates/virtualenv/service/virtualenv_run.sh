#!/bin/sh

# Variables
VIRTUALENVDIR={{ virtualenvdir }}
source_dir={{ source_dir }}

COMMAND=$@

# Modify path
PATH="$VIRTUALENVDIR/bin:$source_dir:$PATH"

# Run custom command
export PATH
cd $source_dir && $COMMAND
