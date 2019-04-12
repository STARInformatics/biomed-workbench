#!/usr/bin/bash

if [ -n "$1" ]; then
    export BKW_BASE_URL=$1
else
    export BKW_BASE_URL=http://localhost:5000
fi
echo "BKW_BASE_URL set to ${BKW_BASE_URL}"

if [ -n "$2" ]; then
    export BKW_API_PATH=$2
fi
echo "BKW_API_PATH set to ${BKW_API_PATH}"

PYTHON3=`command -v python3`
if [ -n "$PYTHON3" ]; then
    export PYTHON3_PATH=${PYTHON3}
else
    export PYTHON3_PATH=`command -v python`
fi

echo "PYTHON3_PATH set to ${PYTHON3_PATH}"

export PIP3_PATH=`command -v pip3`
echo "PIP3_PATH set to ${PIP3_PATH}"

#
# Not run in Makefile anymore
#
#export VIRTUALENV_PATH=`command -v virtualenv`
#echo "VIRTUALENV_PATH set to ${VIRTUALENV_PATH}"
