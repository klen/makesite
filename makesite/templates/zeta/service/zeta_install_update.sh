#!/bin/sh
ZETA_STATICDIR={{ project_staticdir }}

# Check zeta-library
which zeta 1>/dev/null || {
    echo -e "  * Python zetalibrary not found! Attempting to install..."
    sudo pip install zetalibrary
}

sudo zeta $ZETA_STATICDIR
