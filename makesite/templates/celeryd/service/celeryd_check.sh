#!/bin/bash

source {{ project_servicedir }}/.bsfl

# Check supervisor installed
check_program supervisord
check_program supervisorctl
