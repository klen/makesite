#!/bin/sh

# Check uwsgi and install if not exist
which uwsgi 1>/dev/null || {
    sudo pip install http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
}
