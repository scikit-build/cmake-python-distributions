#!/bin/bash

set -e
set -x

MANYLINUX_PYTHON_BIN=/opt/python/cp38-cp38/bin
export PATH="${MANYLINUX_PYTHON_BIN}:$PATH"

cd /io
./scripts/manylinux-build-and-install-openssl.sh

ci_before_install() {
    ${MANYLINUX_PYTHON_BIN}/python scripts/ssl-check.py
    ${MANYLINUX_PYTHON_BIN}/pip install scikit-ci scikit-ci-addons scikit-build
}

ci_install() {
    ${MANYLINUX_PYTHON_BIN}/ci install
}
ci_test() {
    ${MANYLINUX_PYTHON_BIN}/ci test
}
ci_after_success() {
    ${MANYLINUX_PYTHON_BIN}/ci after_test
}

ci_before_install
ci_install
ci_test
ci_after_success
