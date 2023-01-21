
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2.tar.gz")
set(unix_source_sha256       "c026f22cb931dd532f648f087d587f07a1843c6e66a3dfca4fb0ea21944ed33c")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2.zip")
set(windows_source_sha256    "2781c207c3c64ea8a829b8fc0229374fc874b68fb1264cff99055e5bce79bbae")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "783da74f132fd1fea91b8236d267efa4df5b91c5eec1dea0a87f0cf233748d99")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "a988e2a69c1d105987f12782ee0fa80d6be941b3e1a68b4bd6a661f0fdb56d75")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-windows-i386.zip")
set(win32_binary_sha256      "833abaa21bb673491def058cc38834fbd606d525ab271f37a3b8a3aed586c4a0")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-windows-x86_64.zip")
set(win64_binary_sha256      "0db9d3cebf894f64751141253fb9d9e310f325e2e03044f61249a359d6adf301")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-windows-arm64.zip")
set(winarm64_binary_sha256   "c54fb253ae184b391d5366b958c38b282d5f9b6a5854643c28e6887f5fd92590")
