VIRTUALENVDIR={{ virtualenv  }}
PIP_PROJECTFILE={{ pip_projectfile }}

# Check pip
type -P pip &>/dev/null || { echo "I require pip but it's not installed.  Aborting." >&2; exit 1; }

if [ -f $PIP_PROJECTFILE ]; then
    echo "Update virtualenv requirements '$PIP_PROJECTFILE'."
    sudo pip -E $VIRTUALENVDIR install -r $PIP_PROJECTFILE
fi
