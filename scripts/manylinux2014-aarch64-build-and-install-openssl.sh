#!/usr/bin/env bash

#
# Configure, build and install OpenSSL to support building of CMake using manylinux2014-aarch64 docker image
#

set -eux
set -o pipefail

MY_DIR=$(dirname "${BASH_SOURCE[0]}")
source $MY_DIR/utils.sh

OPENSSL_ROOT=openssl-1.1.1g

# Hash from https://www.openssl.org/source/openssl-1.1.1g.tar.gz.sha256
OPENSSL_HASH=ddb04774f1e32f0c49751e21b67216ac87852ceb056b75209af2443400636d46

# Environment variables defined in "dockcross/manylinux2014-aarch64/Dockerfile.in"
check_var CROSS_ROOT
check_var CROSS_TRIPLE

OPENSSL_INSTALL_DIR=${CROSS_ROOT}/${CROSS_TRIPLE}

cd /tmp

# Download
wget http://www.openssl.org/source/${OPENSSL_ROOT}.tar.gz
check_sha256sum ${OPENSSL_ROOT}.tar.gz ${OPENSSL_HASH}
tar -xzf ${OPENSSL_ROOT}.tar.gz
rm -rf ${OPENSSL_ROOT}.tar.gz

# Configure
cd ${OPENSSL_ROOT}
./Configure \
  linux-aarch64 \
  --cross-compile-prefix= \
  --prefix=${OPENSSL_INSTALL_DIR} \
  shared

# Build
make -j$(grep -c processor /proc/cpuinfo)

# Install
make install

