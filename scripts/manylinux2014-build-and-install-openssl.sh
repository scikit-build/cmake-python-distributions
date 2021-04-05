#!/usr/bin/env bash

#
# Configure, build and install OpenSSL to support building of CMake using manylinux2014-aarch64 docker image
#

set -eux
set -o pipefail

MY_DIR=$(dirname "${BASH_SOURCE[0]}")
source $MY_DIR/utils.sh

OPENSSL_ROOT=openssl-1.1.1k

# Hash from https://www.openssl.org/source/openssl-1.1.1k.tar.gz.sha256
OPENSSL_HASH=892a0875b9872acd04a9fde79b1f943075d5ea162415de3047c327df33fbaee5

# Environment variables defined in "dockcross/manylinux2014-aarch64/Dockerfile.in"
check_var CROSS_ROOT
check_var CROSS_TRIPLE

# OPENSSL_INSTALL_DIR=${CROSS_ROOT}/${CROSS_TRIPLE}
# Support using older manylinux2014-aarch64 images where 'sudo' is broken

OPENSSL_INSTALL_DIR=$1
shift

cd /tmp

# Download
curl -fsSLO http://www.openssl.org/source/${OPENSSL_ROOT}.tar.gz
check_sha256sum ${OPENSSL_ROOT}.tar.gz ${OPENSSL_HASH}
tar -xzf ${OPENSSL_ROOT}.tar.gz
rm -rf ${OPENSSL_ROOT}.tar.gz

if [ "$(uname -m)" == "s390x" ]; then
  TARGET=linux64-s390x
else
  TARGET=linux-$(uname -m)
fi

# Configure
cd ${OPENSSL_ROOT}
./Configure \
  ${TARGET} \
  --cross-compile-prefix= \
  --prefix=${OPENSSL_INSTALL_DIR} \
  $*

# Build
make -j$(nproc)

# Install
make install > /dev/null

cd /tmp
rm -rf ${OPENSSL_ROOT}
