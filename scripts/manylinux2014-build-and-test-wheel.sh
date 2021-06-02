#!/bin/bash

set -e
set -x

MANYLINUX_PYTHON_BIN=/opt/python/cp38-cp38/bin
export PATH="${MANYLINUX_PYTHON_BIN}:$PATH"

cd /io
./scripts/manylinux2014-build-and-install-openssl.sh /tmp/openssl-install shared

MACHINE=$(uname -m)
if [ "${MACHINE}" == "s390x" ] || [ "${MACHINE}" == "ppc64le" ]; then
    # build cryptography from sources
    yum install -y libffi-devel
    curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable --profile minimal --no-modify-path
    export PATH=${HOME}/.cargo/bin:${PATH}
    ./scripts/manylinux2014-build-and-install-openssl.sh /tmp/openssl-cryptography no-shared -fPIC
    CFLAGS="-I/tmp/openssl-cryptography/include" LDFLAGS="-L/tmp/openssl-cryptography/lib" ${MANYLINUX_PYTHON_BIN}/pip wheel --no-binary :all: cryptography
    ${MANYLINUX_PYTHON_BIN}/pip install ./cryptography*.whl
fi

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
