VIRTUALENVDIR={{ virtualenv  }}
PIP_PROJECTFILE={{ pip_projectfile }}

# Check pip
if ! which pip >/dev/null; then echo "  * I require pip but it's not installed."; exit 0; fi

if [ -f $PIP_PROJECTFILE ]; then
    echo "Update virtualenv requirements '$PIP_PROJECTFILE'."
    sudo pip -E $VIRTUALENVDIR install -r $PIP_PROJECTFILE
fi
