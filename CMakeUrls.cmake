
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0.tar.gz")
set(unix_source_sha256       "ddc54ad63b87e153cf50be450a6580f1b17b4881de8941da963ff56991a4083b")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0.zip")
set(windows_source_sha256    "7691fb5621e4852d1561cc81d5a09cea6fdff646d4d12d2e893b2c0d4ea4dd10")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "a06e6e32da747e569162bc0442a3fd400fadd9db7d4f185c9e4464ab299a294b")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "94c92c76ac861da7e450d44805be828a8c9b2c3c5dd75144c91248fe1d177eea")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0-windows-i386.zip")
set(win32_binary_sha256      "28408c0ca3b4461550bbcad94c526846699ed79366d81b57db0375cb119875dd")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0-windows-x86_64.zip")
set(win64_binary_sha256      "89e87f3e297b70f1349ee7c5f90783ca96efb986b70c558c799c3c9b1b716456")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0-windows-arm64.zip")
set(winarm64_binary_sha256   "6a24f1ea0965a10a2508b16db1ec8b62c83d5323ac33a1aa7d201797ba147302")
