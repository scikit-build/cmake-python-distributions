#!/bin/bash
set -e -x

# Build standalone project and populate archive cache
mkdir -p /work/archive-cache
mkdir -p /work/standalone-build
pushd /work/standalone-build > /dev/null 2>&1
  cmake -DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/work/archive-cache -G Ninja ../
  ninja
popd > /dev/null 2>&1

# Compile wheels re-using standalone project and archive cache
for PYBIN in /opt/python/*/bin; do
    if [[ ${PYBIN} == *"cp26"* ]]; then
        echo "Skipping ${PYBIN}"
        continue
    fi
    ${PYBIN}/pip install --user -r /work/requirements-dev.txt
    ${PYBIN}/python setup.py bdist_wheel -- \
      -DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/work/archive-cache \
      -DCMakeProject_BINARY_DIR:PATH=/work/standalone-build
    ${PYBIN}/python setup.py clean
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    if [[ ${PYBIN} == *"cp26"* ]]; then
        echo "Skipping ${PYBIN}"
        continue
    fi
    ${PYBIN}/pip install cmake --no-index -f /work/dist
    (cd $HOME; ${PYBIN}/cmake --version)
done
