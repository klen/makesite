USER={{ user }}
BRANCH={{ branch }}
PROJECT={{ project }}
BASERUN={{ deploy_dir }}/service/base_run.sh
TEST_FILE={{ deploy_dir }}/source/.tests

if [ "$BRANCH" = "master" ] || [ "$BRANCH" = "test" ]; then
    if [ -f $BASE_RUN ] && [ -f $TEST_FILE ]; then
        command=$(cat $TEST_FILE)
        echo "  * Run tests for $PROJECT."
        sudo -u $USER sh $BASERUN $command
    fi
else
    echo "  * Auto tests run only for master, test branches."
    exit 0
fi

