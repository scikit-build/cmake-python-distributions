#!/usr/bin/env bash

#
# Configure, build and install OpenSSL to support building of CMake using manylinux docker images
#

set -eux
set -o pipefail

MY_DIR=$(dirname "${BASH_SOURCE[0]}")
source $MY_DIR/utils.sh

OPENSSL_ROOT=openssl-1.1.1k
# Hash from https://www.openssl.org/source/openssl-1.1.1k.tar.gz.sha256
OPENSSL_HASH=892a0875b9872acd04a9fde79b1f943075d5ea162415de3047c327df33fbaee5

OPENSSL_ARCHIVE=/host/${OPENSSL_CACHE_DIR}/${OPENSSL_ROOT}-manylinux-$(uname -m).tar.gz

mkdir -p "$(dirname ${OPENSSL_ARCHIVE})"

if [ -e "${OPENSSL_ARCHIVE}" ]; then
	if ! [ -f "${OPENSSL_ARCHIVE}" ]; then
		echo "'${OPENSSL_ARCHIVE}' is not a file !" 1>&2
		exit 1
	fi
	if ! [ -r "${OPENSSL_ARCHIVE}" ]; then
		echo "'${OPENSSL_ARCHIVE}' is not readable !" 1>&2
		exit 1
	fi
fi

if ! [ -e "${OPENSSL_ARCHIVE}" ]; then
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
	fi

	# Download
	curl -fsSLO http://www.openssl.org/source/${OPENSSL_ROOT}.tar.gz
	check_sha256sum ${OPENSSL_ROOT}.tar.gz ${OPENSSL_HASH}
	tar -xzf ${OPENSSL_ROOT}.tar.gz
	rm -rf ${OPENSSL_ROOT}.tar.gz

	# Configure
	pushd ${OPENSSL_ROOT}
	./config no-shared -fPIC --prefix=/usr/local/ssl --openssldir=/usr/local/ssl > /dev/null

	# Build
	make -j$(nproc) > /dev/null

	# Install
	make install_sw DESTDIR=/tmp/${OPENSSL_ROOT}-root > /dev/null
	tar -C /tmp/${OPENSSL_ROOT}-root -czf "${OPENSSL_ARCHIVE}" usr

	popd
	rm -rf ${OPENSSL_ROOT}
fi

tar -C / -xf "${OPENSSL_ARCHIVE}"
