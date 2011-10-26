#!/bin/bash

source {{ project_servicedir }}/.bsfl

# Check uwsgi
check_program uwsgi
