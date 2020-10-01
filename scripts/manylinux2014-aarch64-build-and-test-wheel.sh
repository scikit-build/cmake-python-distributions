#!/bin/bash

set -e
set -x

MANYLINUX_PYTHON=cp38-cp38
export PATH="/opt/python/${MANYLINUX_PYTHON}/bin:$PATH"

yum install -y wget

cd /io
./scripts/manylinux2014-aarch64-build-and-install-openssl.sh

ci_before_install() {
    /opt/python/${MANYLINUX_PYTHON}/bin/python scripts/ssl-check.py
    /opt/python/${MANYLINUX_PYTHON}/bin/pip install scikit-ci scikit-ci-addons scikit-build
}

ci_install() {
    /opt/python/${MANYLINUX_PYTHON}/bin/ci install
}
ci_test() {
    /opt/python/${MANYLINUX_PYTHON}/bin/ci test
}
ci_after_success() {
    /opt/python/${MANYLINUX_PYTHON}/bin/ci after_test
}

ci_before_install
ci_install
ci_test
ci_after_success
