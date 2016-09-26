#!/bin/bash
set -e -x

# i686 or x86_64 ?
case $(uname -p) in
    i686)
        arch=x86
        ;;
    x86_64)
        arch=x64
        ;;
    *)
        die "Unknown architecture $(uname -p)"
        ;;
esac

echo "Building wheels for $arch"

# Build standalone project and populate archive cache
mkdir -p /work/archive-cache
mkdir -p /work/standalone-${arch}-build
pushd /work/standalone-${arch}-build > /dev/null 2>&1
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
      -DCMakeProject_BINARY_DIR:PATH=/work/standalone-${arch}-build
    ${PYBIN}/python setup.py clean
done

# Since there are no external shared libraries to bundle into the wheels
# this step will fixup the wheel switching from 'linux' to 'manylinux1' tag
for whl in dist/*$(uname -p).whl; do
    auditwheel repair $whl -w /work/dist/
    rm $whl
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    if [[ ${PYBIN} == *"cp26"* ]]; then
        echo "Skipping ${PYBIN}"
        continue
    fi
    sudo ${PYBIN}/pip install cmake --no-cache-dir --no-index -f /work/dist
    (cd $HOME; ${PYBIN}/cmake --version)
done
