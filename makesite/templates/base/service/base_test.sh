#!/bin/sh

# Variables
SITE_USER={{ site_user }}
BRANCH={{ branch }}
PROJECT={{ project }}
BASERUN={{ project_servicedir }}/base_run.sh
TEST_FILE={{ project_sourcedir }}/.tests


# Test project
if [ "$BRANCH" = "master" ] || [ "$BRANCH" = "test" ]; then
    if [ -f $BASE_RUN ] && [ -f $TEST_FILE ]; then
        command=`cat $TEST_FILE`
        echo "  * Run tests for $PROJECT."
        sudo -u $SITE_USER sh $BASERUN $command
    fi
else
    echo "  * Auto tests run only for master, test branches."
    exit 0
fi
