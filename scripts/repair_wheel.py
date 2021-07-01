#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from convert_to_generic_platform_wheel import convert_to_generic_platform_wheel


def main():
    if sys.platform.startswith("linux"):
        os_ = "linux"
    elif sys.platform.startswith("darwin"):
        os_ = "macos"
    elif sys.platform.startswith("win32"):
        os_ = "windows"
    else:
        raise NotImplementedError("sys.platform '{}' is not supported yet.".format(sys.platform))

    p = argparse.ArgumentParser(description="Convert wheel to be independent of python implementation and ABI")
    p.set_defaults(prog=Path(sys.argv[0]).name)
    p.add_argument("WHEEL_FILE", help="Path to wheel file.")
    p.add_argument(
        "-w",
        "--wheel-dir",
        dest="WHEEL_DIR",
        help=('Directory to store delocated wheels (default: "wheelhouse/")'),
        default="wheelhouse/",
    )

    args = p.parse_args()

    file = Path(args.WHEEL_FILE).resolve(strict=True)
    wheelhouse = Path(args.WHEEL_DIR).resolve()
    wheelhouse.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir_:
        tmpdir = Path(tmpdir_)
        # use the platform specific repair tool first
        if os_ == "linux":
            subprocess.run(["auditwheel", "repair", "-w", str(tmpdir), str(file)], check=True, stdout=subprocess.PIPE)
        elif os_ == "macos":
            # delocate does not pass for now: https://github.com/matthew-brett/delocate/issues/105
            # subprocess.run(
            #     ["delocate-wheel", "--require-archs", "arm64,x86_64", "-w", str(tmpdir), str(file)],
            #     check=True,
            #     stdout=subprocess.PIPE,
            # )
            shutil.copyfile(file, tmpdir / file.name)
        elif os_ == "windows":
            # no specific tool, just copy
            shutil.copyfile(file, tmpdir / file.name)
        (file,) = tmpdir.glob("*.whl")

        # we need to handle macOS universal2 & arm64 here for now, let's use additional_platforms for this.
        additional_platforms = []
        if os_ == "macos":
            # first, get the target macOS deployment target from the wheel
            match = re.match(r"^.*-macosx_(\d+)_(\d+)_x86_64\.whl$", file.name)
            assert match is not None
            target = tuple(map(int, match.groups()))

            # let's add universal2 platform for this wheel.
            additional_platforms = ["macosx_{}_{}_universal2".format(*target)]

            # given pip support for universal2 was added after arm64 introduction
            # let's also add arm64 platform.
            arm64_target = target
            if arm64_target < (11, 0):
                arm64_target = (11, 0)
            additional_platforms.append("macosx_{}_{}_arm64".format(*arm64_target))

            if target < (11, 0):
                # They're were also issues with pip not picking up some universal2 wheels, tag twice
                additional_platforms.append("macosx_11_0_universal2")

        # make this a py2.py3 wheel
        convert_to_generic_platform_wheel(
            str(file),
            out_dir=str(wheelhouse),
            py2_py3=True,
            additional_platforms=additional_platforms,
        )


if __name__ == "__main__":
    main()
