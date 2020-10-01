#!/usr/bin/env bash

#
# Configure, build and install OpenSSL to support building of CMake using manylinux2014-aarch64 docker image
#

set -eux
set -o pipefail

MY_DIR=$(dirname "${BASH_SOURCE[0]}")
source $MY_DIR/utils.sh

OPENSSL_ROOT=openssl-1.1.1h

# Hash from https://www.openssl.org/source/openssl-1.1.1h.tar.gz.sha256
OPENSSL_HASH=5c9ca8774bd7b03e5784f26ae9e9e6d749c9da2438545077e6b3d755a06595d9

# Environment variables defined in "dockcross/manylinux2014-aarch64/Dockerfile.in"
check_var CROSS_ROOT
check_var CROSS_TRIPLE

# OPENSSL_INSTALL_DIR=${CROSS_ROOT}/${CROSS_TRIPLE}
# Support using older manylinux2014-aarch64 images where 'sudo' is broken
OPENSSL_INSTALL_DIR=/tmp/openssl-install

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
make -j$(nproc)

# Install
make install

