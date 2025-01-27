
#-----------------------------------------------------------------------------
# CMake sources
set(unix_source_url          "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5.tar.gz")
set(unix_source_sha256       "66fb53a145648be56b46fa9e8ccade3a4d0dfc92e401e52ce76bdad1fea43d27")

set(windows_source_url       "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5.zip")
set(windows_source_sha256    "761ea241c42a0ea0b2bea45d797d29233b8f239b004ae2dc8b7d76306dc5dfc0")

#-----------------------------------------------------------------------------
# CMake binaries

set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
set(linux32_binary_sha256    "NA")

set(linux64_binary_url       "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5-linux-x86_64.tar.gz")
set(linux64_binary_sha256    "2984e70515ff60c5e4a41922b5d715a8168a696a89721e3b114e36f453244f72")

set(macos10_10_binary_url    "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5-macos10.10-universal.tar.gz")
set(macos10_10_binary_sha256 "1b5ebc625e981701e2ab3061e0ebb745b848b55536502293621ee676aefdcf1d")

set(win32_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5-windows-i386.zip")
set(win32_binary_sha256      "26183bb30c7e338804570392426bc9abfe0e7bfc79bf27cd2d9ade9a5ba6a39f")

set(win64_binary_url         "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5-windows-x86_64.zip")
set(win64_binary_sha256      "d4d2d4b9ccd68dae975a066fcd42ea9807ef40f79ee6971923fd3788e7917585")

set(winarm64_binary_url      "https://github.com/Kitware/CMake/releases/download/v3.31.5/cmake-3.31.5-windows-arm64.zip")
set(winarm64_binary_sha256   "a734e4e970fdaa4b5957157c059556f56ca5d655014cd4b5fd9194aaba316f31")
