#!/bin/sh

SITE_USER={{ site_user }}
SITE_GROUP={{ site_group }}
PROJECT_STATICDIR={{ project_staticdir }}

# Check zeta-library
which zeta 1>/dev/null || {
    echo -e "  * Python zetalibrary not found! Attempting to install..."
    sudo pip install zetalibrary
}

sudo zeta $PROJECT_STATICDIR

# Restore rights
sudo chown -R $SITE_USER:$SITE_GROUP $PROJECT_STATICDIR
