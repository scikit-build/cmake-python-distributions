
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4.tar.gz")
set(unix_source_sha256       "b1b48d7100bdff0b46e8c8f6a3c86476dbe872c8df39c42b8d104298b3d56a2c")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4.zip")
set(windows_source_sha256    "be6aa7238a19f3ab9d135ca3111ccd17c4862a5eb9543ecffe5926e09f4390f6")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "64e5473169dd43055fbf2c138cae6e5ec10f30a0606d24f12078e68466320cf4")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "44a59c584122676463bf5bdd2c7dee2ac02944e065a71cc30c57541a20d3465c")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4-windows-i386.zip")
set(win32_binary_sha256      "8773df8f82a8172cfd964cc052864592d45481a636cb8b533e3736102a97c2fa")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4-windows-x86_64.zip")
set(win64_binary_sha256      "1c8bfbc5537553edccded62f8f03475a161280c1b64f54c887824c6eb4e773ff")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v3.29.4/cmake-3.29.4-windows-arm64.zip")
set(winarm64_binary_sha256   "16ce291dd34189a60d7add96b4148adfdbb46b6b2478086cb43abe2e5ff34ad3")
