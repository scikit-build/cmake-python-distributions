#!/bin/bash

# Stop at any error, show all commands
set -exuo pipefail

TOOLCHAIN_PATH=/opt/clang

# Download static-clang
DEFAULT_ARCH="$(uname -m)"
if [ "${STATIC_CLANG_ARCH:-}" == "" ]; then
	STATIC_CLANG_ARCH="${RUNNER_ARCH:-${DEFAULT_ARCH}}"
fi
case "${STATIC_CLANG_ARCH}" in
	ARM64|aarch64|arm64|arm64/*) GO_ARCH=arm64;;
	ARM|armv7l|armv8l|arm|arm/v7) GO_ARCH=arm;;  # assume arm/v7 for arm
	X64|x86_64|amd64|amd64/*) GO_ARCH=amd64;;
	X86|i686|386) GO_ARCH=386;;
	ppc64le) GO_ARCH=ppc64le;;
	riscv64) GO_ARCH=riscv64;;
	s390x) GO_ARCH=s390x;;
	*) echo "No static-clang toolchain for ${CLANG_ARCH}">2; exit 1;;
esac
STATIC_CLANG_VERSION=20.1.8.0
STATIC_CLANG_FILENAME="static-clang-linux-${GO_ARCH}.tar.xz"
STATIC_CLANG_URL="https://github.com/mayeut/static-clang-images/releases/download/v${STATIC_CLANG_VERSION}/${STATIC_CLANG_FILENAME}"
pushd /tmp
cat<<'EOF' | grep "${STATIC_CLANG_FILENAME}" > "${STATIC_CLANG_FILENAME}.sha256"
5ef070163055340d5bbf11263e60396b4f221c7dab90e167424e1b9b68a6048e  static-clang-linux-386.tar.xz
3a25cb4eae724cad96d7e504ce7669a824f61d57d27716fd47d0a9f1fe2d8fdf  static-clang-linux-amd64.tar.xz
250e5cc18fb7b6f7a4a0d8fe63ddf8a885f7351c4be7e4a164f4c04dfbee5a7f  static-clang-linux-arm.tar.xz
da56c2b13a0c3e676e010d61a87753a975de18ae9eaa65247ca6a6d22bb95ab4  static-clang-linux-arm64.tar.xz
466af6ca1be0cd4f2ae6704ce5ae0f86a1648e999756def1680b639bc63d2916  static-clang-linux-ppc64le.tar.xz
8078365b22f1d5290db7e60501daa80c91da8d530720d3fc974ab3f81e56bae5  static-clang-linux-riscv64.tar.xz
97e933c45a35c827530888e1c2f6b6eee0140ccb2089fdfdf9f99454d4c470e0  static-clang-linux-s390x.tar.xz
EOF
curl -fsSLO "${STATIC_CLANG_URL}"
sha256sum -c "${STATIC_CLANG_FILENAME}.sha256"
tar -C /opt -xf "${STATIC_CLANG_FILENAME}"
popd

# configure target triple
case "${AUDITWHEEL_POLICY}-${AUDITWHEEL_ARCH}" in
	manylinux*-armv7l) TARGET_TRIPLE=armv7-unknown-linux-gnueabihf;;
	musllinux*-armv7l) TARGET_TRIPLE=armv7-alpine-linux-musleabihf;;
	manylinux*-ppc64le) TARGET_TRIPLE=powerpc64le-unknown-linux-gnu;;
	musllinux*-ppc64le) TARGET_TRIPLE=powerpc64le-alpine-linux-musl;;
	manylinux*-*) TARGET_TRIPLE=${AUDITWHEEL_ARCH}-unknown-linux-gnu;;
	musllinux*-*) TARGET_TRIPLE=${AUDITWHEEL_ARCH}-alpine-linux-musl;;
esac
case "${AUDITWHEEL_ARCH}" in
	riscv64) M_ARCH="-march=rv64gc";;
	x86_64) M_ARCH="-march=x86-64";;
	armv7l) M_ARCH="-march=armv7a";;
	i686) M_ARCH="-march=i686";;
esac
GCC_TRIPLE=$(gcc -dumpmachine)

if [ "${AUDITWHEEL_ARCH}" == "riscv64" ]; then
	# the LDFLAGS from pyproject.toml seems not to be taken into account when building CMake (no problem with OpenSSL)
	# FAILED: [code=1] Source/kwsys/cmsysTestProcess
	#  : && /opt/clang/bin/clang -D_POSIX_C_SOURCE=199506L -D_POSIX_SOURCE=1 -D_SVID_SOURCE=1 -D_BSD_SOURCE=1 -O3 -DNDEBUG  -lstdc++ -lgcc -lrt Source/kwsys/CMakeFiles/cmsysTestProcess.dir/testProcess.c.o  -o Source/kwsys/cmsysTestProcess  Source/kwsys/libcmsys_c.a && :
	#  /usr/bin/riscv64-linux-gnu-ld: -march=rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0: unsupported ISA subset `z'
	#  /usr/bin/riscv64-linux-gnu-ld: failed to merge target specific data of file Source/kwsys/libcmsys_c.a(ProcessUNIX.c.o)
	#  /usr/bin/riscv64-linux-gnu-ld: -march=rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0: unsupported ISA subset `z'
	#  /usr/bin/riscv64-linux-gnu-ld: failed to merge target specific data of file Source/kwsys/libcmsys_c.a(System.c.o)
	#  clang: error: linker command failed with exit code 1 (use -v to see invocation)
	IMPLICIT_LLD="-fuse-ld=lld"
fi

cat<<EOF >"${TOOLCHAIN_PATH}/bin/${AUDITWHEEL_PLAT}.cfg"
	-target ${TARGET_TRIPLE}
	${M_ARCH:-}
	--gcc-toolchain=${DEVTOOLSET_ROOTPATH:-}/usr
	--gcc-triple=${GCC_TRIPLE}
	${IMPLICIT_LLD:-}
EOF

cat<<EOF >"${TOOLCHAIN_PATH}/bin/clang.cfg"
	@${AUDITWHEEL_PLAT}.cfg
EOF

cat<<EOF >"${TOOLCHAIN_PATH}/bin/clang++.cfg"
	@${AUDITWHEEL_PLAT}.cfg
EOF

cat<<EOF >"${TOOLCHAIN_PATH}/bin/clang-cpp.cfg"
	@${AUDITWHEEL_PLAT}.cfg
EOF

# override entrypoint to add the toolchain to PATH
mv /usr/local/bin/manylinux-entrypoint /usr/local/bin/manylinux-entrypoint-org
cat<<EOF >/usr/local/bin/manylinux-entrypoint
#!/bin/bash

set -eu

export PATH="${TOOLCHAIN_PATH}/bin:\${PATH}"
exec /usr/local/bin/manylinux-entrypoint-org "\$@"
EOF

chmod +x /usr/local/bin/manylinux-entrypoint
