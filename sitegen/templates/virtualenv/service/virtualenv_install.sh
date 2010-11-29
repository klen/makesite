VIRTUALENVDIR={{ virtualenvdir }}
PIP_PROJECTFILE={{ pip_projectfile }}
PYTHON_PREFIX={{ python_prefix }}

# Check virtualenv
which virtualenv 1>/dev/null || { echo "ERROR: * I require virtualenv but it's not installed."; exit 0; }

_psycopg_to_ve () {
    psycopg=`python -c "import psycopg2 as mod;print mod.__path__[0]"`
    mx=`python -c "import mx as mod;print mod.__path__[0]"`
    if [ -d $psycopg ] && [ -d $mx ]; then
        echo "  * Create links to psycopg and mx in virtualenv."
        sudo ln -sf $psycopg $VIRTUALENVDIR/lib/$PYTHON_PREFIX
        sudo ln -sf $mx $VIRTUALENVDIR/lib/$PYTHON_PREFIX
    fi    
}

_pylint_to_ve () {
    pylint=`python -c "import pylint as mod;print mod.__path__[0]"`
    logilab=`python -c "import logilab as mod;print mod.__path__[0]"`
    if [ -d $pylint ] && [ -d $logilab ]; then
        echo "  * Create links to pylint and logilab in virtualenv."
        sudo ln -sf $pylint $VIRTUALENVDIR/lib/$PYTHON_PREFIX
        sudo ln -sf $logilab $VIRTUALENVDIR/lib/$PYTHON_PREFIX
    fi    
}

echo '  * Create virtualenv:'$VIRTUALENVDIR
sudo virtualenv --no-site-packages $VIRTUALENVDIR
_psycopg_to_ve
_pylint_to_ve

which pip 1>/dev/null || { echo "ERROR: * I require pip but it's not installed."; exit 0; }

if [ -f $PIP_PROJECTFILE ]; then
    echo "Update virtualenv requirements '$PIP_PROJECTFILE'."
    sudo pip -E $VIRTUALENVDIR install -r $PIP_PROJECTFILE
    sudo rm -rf $VIRTUALENVDIR/.reqsum && sudo sh -c "md5sum $PIP_PROJECTFILE > $VIRTUALENVDIR/.reqsum"
fi
