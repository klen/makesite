VIRTUALENVDIR={{ virtualenvdir }}
PIP_PROJECTFILE={{ pip_projectfile }}
PYTHONPREFIX=python2.6

# Check virtualenv
if ! which virtualenv >/dev/null; then echo "  * I require virtualenv but it's not installed."; exit 0; fi

_psycopg_to_ve () {
    psycopg_path=/usr/lib/$PYTHONPREFIX/dist-packages/psycopg2
    mx_path=/usr/lib/$PYTHONPREFIX/dist-packages/mx
    if [ -d $psycopg_path ]; then
        echo "  * Create links to psycopg in virtualenv."
        sudo ln -sf $psycopg_path $VIRTUALENVDIR/lib/$PYTHONPREFIX
        sudo ln -sf $mx_path $VIRTUALENVDIR/lib/$PYTHONPREFIX
    fi    
}

echo '  * Create virtualenv:'$VIRTUALENVDIR
sudo virtualenv --no-site-packages $VIRTUALENVDIR
_psycopg_to_ve

# Check pip
if ! which pip >/dev/null; then echo "  * I require pip but it's not installed."; exit 0; fi

if [ -f $PIP_PROJECTFILE ]; then
    echo "Update virtualenv requirements '$PIP_PROJECTFILE'."
    sudo pip -E $VIRTUALENVDIR install -r $PIP_PROJECTFILE
fi
