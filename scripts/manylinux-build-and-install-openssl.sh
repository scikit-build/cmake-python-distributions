#!/usr/bin/env bash

#
# Configure, build and install OpenSSL to support building of CMake using manylinux docker images
#

set -eux
set -o pipefail

MY_DIR=$(dirname "${BASH_SOURCE[0]}")
source $MY_DIR/utils.sh

OPENSSL_ROOT=openssl-3.0.15
OPENSSL_HASH=23c666d0edf20f14249b3d8f0368acaee9ab585b09e1de82107c66e1f3ec9533

cd /tmp

if ! perl -e 'use 5.10.0' &> /dev/null; then
	# perl>=5.10.0 is needed to build openssl
	PERL_ROOT=perl-5.32.1
	# Hash from https://www.cpan.org/src/5.0/perl-5.32.1.tar.gz.sha256.txt
	PERL_HASH=03b693901cd8ae807231b1787798cf1f2e0b8a56218d07b7da44f784a7caeb2c

	curl -fsSLO https://www.cpan.org/src/5.0/${PERL_ROOT}.tar.gz
	check_sha256sum ${PERL_ROOT}.tar.gz ${PERL_HASH}
	tar -xzf ${PERL_ROOT}.tar.gz
	rm -rf ${PERL_ROOT}.tar.gz

	pushd ${PERL_ROOT}
	./Configure -des -Dprefix=/tmp/perl-openssl > /dev/null
	make -j$(nproc) > /dev/null
	make install > /dev/null
	popd
	export PATH=/tmp/perl-openssl/bin:${PATH}
else
	if [ "${AUDITWHEEL_PLAT:0:9}" == "manylinux" ] && command -v yum >/dev/null 2>&1; then
		# more perl modules are needed than the bare minimum already installed in CentOS
		# c.f. https://github.com/openssl/openssl/blob/openssl-3.0.0/NOTES-PERL.md#general-notes
		yum -y install perl-core
	fi
fi

# Download
curl -fsSLO https://github.com/openssl/openssl/releases/download/${OPENSSL_ROOT}/${OPENSSL_ROOT}.tar.gz
check_sha256sum ${OPENSSL_ROOT}.tar.gz ${OPENSSL_HASH}
tar -xzf ${OPENSSL_ROOT}.tar.gz
rm -rf ${OPENSSL_ROOT}.tar.gz

# Configure
pushd ${OPENSSL_ROOT}
./config no-shared -fPIC --prefix=/usr/local/ssl --openssldir=/usr/local/ssl > /dev/null

# Build
make -j$(nproc) > /dev/null

# Install
make install_sw > /dev/null

popd
rm -rf ${OPENSSL_ROOT}
