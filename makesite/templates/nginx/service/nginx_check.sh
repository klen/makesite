#!/bin/bash

source {{ project_servicedir }}/.bsfl

# Check nginx
check_program nginx
