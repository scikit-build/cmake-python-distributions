#!/bin/bash

# This script is intended to be used with the dockcross/manylinux-* Docker
# image. It will build wheels for a Python package in the current directory.
# Running:
#
#   dockcross-manylinux-x64 manylinux.sh
#
# will build wheels for all available manylinux versions. Pass in one or
# more binary versions to restrict the wheels built. For example,
#
#   dockcross-manylinux-x64 manylinux.sh cp27-cp27mu
#
# will only build the cp cp27-cp27mu wheel.

shopt -s nullglob

if [ $# -gt 0 ]; then
  declare -a PYTHON_BIN
  for arg in "$@"; do
    if [ -e /opt/python/$arg/bin ]; then
      PYTHON_BIN[${#PYTHON_BIN[@]}+1]=/opt/python/$arg/bin
    else
      echo "Version does not exist: $arg"
      exit 1
    fi
  done
else
  PYTHON_BIN=( /opt/python/*/bin )
fi

set -e -x

for BIN in "${PYTHON_BIN[@]}"; do
  for requirements in *requirements*txt; do
    ${BIN}/pip install -r $requirements
  done
  ${BIN}/pip wheel . -w dist/
  re="/opt/python/([^/]+)/"
  if [[ "${PYTHON_BIN[@]}" =~ $re ]]; then
    version=${BASH_REMATCH[1]}
    for whl in dist/*${version}*.whl; do
      auditwheel repair $whl -w dist/
    done
  fi
done
