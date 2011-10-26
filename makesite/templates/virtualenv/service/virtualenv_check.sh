#!/bin/bash

source {{ project_servicedir }}/.bsfl

# Check pip and virtualenv
check_program pip
check_program virtualenv
