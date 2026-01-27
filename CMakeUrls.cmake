
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3.tar.gz")
set(unix_source_sha256       "7efaccde8c5a6b2968bad6ce0fe60e19b6e10701a12fce948c2bf79bac8a11e9")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3.zip")
set(windows_source_sha256    "444715a33dc8bcb03221fcb4e849b948fc4392005c5abc52e2c7abbcb158374b")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "5bb505d5e0cca0480a330f7f27ccf52c2b8b5214c5bba97df08899f5ef650c23")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "910b965a6fc72928412dd369c957643ff17a0990cc2435a2573b04c1352d9ff3")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-windows-i386.zip")
set(win32_binary_sha256      "ad46d82c99a818a2cdd694fe82bec99f0cb557d864dc5fff5d54d347c7cdd98f")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-windows-x86_64.zip")
set(win64_binary_sha256      "eb4ebf5155dbb05436d675706b2a08189430df58904257ae5e91bcba4c86933c")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-windows-arm64.zip")
set(winarm64_binary_sha256   "751b206b1cf65151b72c525d26267c1d9beebf8fafc365ae00286571d9fd3ed9")
