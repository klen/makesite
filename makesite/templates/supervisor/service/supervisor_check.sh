#!/bin/bash

source {{ project_servicedir }}/.bsfl

# Check supervisor
check_program supervisord
check_program supervisorctl
