if [ -n "$BASH" ] ; then
    _mks_comp () {
        COMPREPLY=( $( \
            COMP_WORDS="${COMP_WORDS[*]}" \
            COMP_CWORD=$COMP_CWORD \
            MAKESITE_AUTO_COMPLETE=1 $1 ) ) 
    }
    complete -o default -F _mks_comp makesite

else
    function _mks_comp {
        local words cword
        read -Ac words
        read -cn cword
        reply=( $( COMP_WORDS="$words[*]" COMP_CWORD=$(( cword-1 )) MAKESITE_AUTO_COMPLETE=1 $words[1] ) )
    }
    compctl -K _mks_comp makesite
fi

_mks_error () {
    echo "ERROR: "$1 1>&2
}

# Verify that the MAKESITE_HOME directory exists
_mks_verify_sites_home () {
    if [ ! -d "$MAKESITE_HOME" ]; then
        _mks_error "Makesite sites directory '$MAKESITE_HOME' does not exist.  Create it or set MAKESITE_HOME to an existing directory."
        return 1
    fi
    return 0
}

# Verify that the requested site exists
_mks_verify_site () {
    if [ ! -d "$1" ]; then
        _mks_error "Project '$1' not found."
        return 1
    fi
    return 0
}

# List of available sites.
_mks_find_sites () {
    _mks_verify_sites_home || return 1
    find $MAKESITE_HOME -maxdepth 3 -name '.makesite' | sed 's|/\.makesite||' | sort
}

# Get sitename
_mks_sitename () {
    if [ -z "$1" ]; then
        return 1
    fi
    branch=`basename $1`
    project=`dirname $1 | xargs basename`
    echo -n $project"."$branch
}

# Change dir to site dir
cdsite () {
    project="$1"
    if [ -z "$1" ]; then
        _mks_verify_sites_home || return 1
        cd $MAKESITE_HOME
    else
        _mks_verify_site $project || return 1
        cd $project
    fi
}

# Activate site virtualenv
envsite () {
    project="$1"
    if [ -z $project ]; then
        project=`echo $PWD | sed 's|/source$||'`
    fi
    activate=$project/.virtualenv/bin/activate

    _mks_verify_sites_home || return 1
    _mks_verify_site $project || return 1

    if [ ! -f "$activate" ]
    then
        _mks_error "Project '`_makesite_showinfo $project`' does not contain an activate script."
        return 1
    fi

    source "$activate"

    # Path virtualenv bash promt
    if [ ! -z "$_OLD_VIRTUAL_PS1" ]; then
        PS1=(`_mks_sitename $project`)$_OLD_VIRTUAL_PS1
        export PS1
    fi
}

# Cahnge dir to site source and activate virtualenv
worksite () {
    project="$1"
    cdsite $1/source
    envsite $1
}

if [ -n "$BASH" ] ; then
    _sites ()
    {
        local cur="${COMP_WORDS[COMP_CWORD]}"
        COMPREPLY=( $(compgen -W "`_mks_find_sites`" -- ${cur}) )
    }

    complete -o default -o nospace -F _sites cdsite
    complete -o default -o nospace -F _sites envsite
    complete -o default -o nospace -F _sites worksite
fi
