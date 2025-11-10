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
STATIC_CLANG_VERSION=21.1.5.0
STATIC_CLANG_FILENAME="static-clang-linux-${GO_ARCH}.tar.xz"
STATIC_CLANG_URL="https://github.com/mayeut/static-clang-images/releases/download/v${STATIC_CLANG_VERSION}/${STATIC_CLANG_FILENAME}"
pushd /tmp
cat<<'EOF' | grep "${STATIC_CLANG_FILENAME}" > "${STATIC_CLANG_FILENAME}.sha256"
7af47b1c41dd1e76e08d33f13f7fe33eb43849040f69499516f3f01708b12ae0  static-clang-linux-386.tar.xz
395463d070de084f249bf08d3a8a88a42f19bce24cad37b45c78d48a62a73bdc  static-clang-linux-amd64.tar.xz
294839579cf4d2fb5343b6ee1e1613f126c765664e253f2109725d5f49db6aa3  static-clang-linux-arm.tar.xz
7476d44530b560c5bdc1b085c8651810c2fece201410d831c47b2d3b8101c1b2  static-clang-linux-arm64.tar.xz
dcdb642827b5da8570b312c1a877bdf4a2b0f7e3004394a3b216134c3178f346  static-clang-linux-loong64.tar.xz
6b247ae1ce6d095375cd4f37a0484f0c91f8457e3c3f3bb7f9c125a414b19bed  static-clang-linux-ppc64le.tar.xz
fb0cce0e1fecceb6d3eb2e095297731107c0803605815b37a5cbcec270700088  static-clang-linux-riscv64.tar.xz
18cbfc7471a40a091b02b2999303dfa3f87368dd01e65d0d3ca7b216826ac84f  static-clang-linux-s390x.tar.xz
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
