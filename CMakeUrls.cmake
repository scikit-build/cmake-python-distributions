
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2.tar.gz")
set(unix_source_sha256       "36db4b6926aab741ba6e4b2ea2d99c9193222132308b4dc824d4123cb730352e")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2.zip")
set(windows_source_sha256    "1bd1ec06a5a27e1ded74e66eb0d24ee6c2639e3456fd39b6c46d63549aedeaa2")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "0416c70cf88e8f92efcbfe292e181bc09ead7d70e29ab37b697522c01121eab5")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "0b542389345b28d2f73122b72ec9b899947e643fd86cf8f42bae2718884d2ad3")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2-windows-i386.zip")
set(win32_binary_sha256      "e51b281c9dfd1498834729b33bf49fc668ad1dadbc2eaba7b693d0f7d748450d")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2-windows-x86_64.zip")
set(win64_binary_sha256      "86b5de51f60a0e9d62be4d8ca76ea467d154083d356fcc9af1409606be341cd8")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v3.29.2/cmake-3.29.2-windows-arm64.zip")
set(winarm64_binary_sha256   "5b16a0db4966c04582c40131038de49d5b0161fcd950dc9e955753dfab858882")
