
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3.tar.gz")
set(unix_source_sha256       "72b7570e5c8593de6ac4ab433b73eab18c5fb328880460c86ce32608141ad5c1")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3.zip")
set(windows_source_sha256    "b54943b9c98ac66061e9b97fd630b3f06a75a85143a561ef2dca88aa0e042c60")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "804d231460ab3c8b556a42d2660af4ac7a0e21c98a7f8ee3318a74b4a9a187a6")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "5541339751cb96d1b03eb3244df7e750cd4e1dcb361ebbd68a179493dfccc5bf")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-windows-i386.zip")
set(win32_binary_sha256      "411812b6b29ac793faf69bdbd36c612f72659363c5491b9f0a478915db3fc58c")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-windows-x86_64.zip")
set(win64_binary_sha256      "cac7916f7e1e73a25de857704c94fd5b72ba9fe2f055356b5602d2f960e50e5b")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-windows-arm64.zip")
set(winarm64_binary_sha256   "cfe023b7e82812ef802fb1ec619f6cfa2fdcb58ee61165fc315086286fe9cdcc")
