#!/bin/sh

SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
VIRTUALENVDIR={{ virtualenvdir }}
PIP_PROJECTFILE={{ pip_projectfile }}
PYTHON_PREFIX={{ python_prefix }}
VIRTUALENV_DEBUG={{ virtualenv_debug }}

# Check easy_install
which easy_install 1>/dev/null || {
    echo "  * Python setuptools not found! Attempting to install..."
    if [ -f /etc/lsb-release ] ; then
            sudo apt-get install python-setuptools
    elif [ -f /etc/fedora-release ] ; then
            sudo yum install python-setuptools
    elif [ -f /etc/debian_version ] ; then
            sudo apt-get install python-setuptools
    fi
}

# Check pip
which pip 1>/dev/null || {
    echo "  * Pip not found! Attempting to install..."
    sudo easy_install -U setuptools
    sudo easy_install -U pip
}

# Check virtualenv
which virtualenv 1>/dev/null || {
    echo "  * Virtualenv not found! Attempting to install..."
    sudo pip install virtualenv
}

_psycopg_to_ve () {
    psycopg=`python -c "import psycopg2 as mod;print mod.__path__[0]"`
    mx=`python -c "import mx as mod;print mod.__path__[0]"`
    if [ -d $psycopg ] && [ -d $mx ]; then
        echo "  * Create links to psycopg and mx in virtualenv."
        sudo ln -sf $psycopg $VIRTUALENVDIR/lib/$PYTHON_PREFIX
        sudo ln -sf $mx $VIRTUALENVDIR/lib/$PYTHON_PREFIX
    fi    
}

_memcache_to_ve () {
    memcache=`python -c "import memcache as mod;print mod.__file__"`
    if [ -f $memcache ]; then
        echo "  * Create links to memcache in virtualenv."
        sudo ln -sf $memcache $VIRTUALENVDIR/lib/$PYTHON_PREFIX
    fi    
}

echo '  * Create virtualenv:'$VIRTUALENVDIR
sudo virtualenv --no-site-packages $VIRTUALENVDIR
_psycopg_to_ve
_memcache_to_ve

if [ -f $PIP_PROJECTFILE ]; then
    echo "  * Update virtualenv requirements '$PIP_PROJECTFILE'."
    sudo pip -E $VIRTUALENVDIR install -I -r $PIP_PROJECTFILE
    sudo rm -rf $VIRTUALENVDIR/.reqsum && sudo sh -c "md5sum $PIP_PROJECTFILE > $VIRTUALENVDIR/.reqsum"
else
    echo "  ! Not found pip requirements file: "$PIP_PROJECTFILE
fi

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $VIRTUALENVDIR
