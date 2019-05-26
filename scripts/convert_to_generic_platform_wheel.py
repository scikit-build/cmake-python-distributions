
import argparse
import glob
import logging
import os
import sys

from itertools import product
from os.path import (abspath, basename, dirname, isfile, join as pjoin, splitext)

from wheel.pkginfo import read_pkg_info, write_pkg_info
from wheel.install import WHEEL_INFO_RE
from wheeltools.tools import unique_by_index
from wheeltools.wheeltools import InWheelCtx, WheelToolsError

logger = logging.getLogger(splitext(basename(__file__))[0])


def _dist_info_dir(bdist_dir):
    """Get the .dist-info directort from an unpacked wheel

    Parameters
    ----------
    bdist_dir : str
        Path of unpacked wheel file
    """

    info_dirs = glob.glob(pjoin(bdist_dir, '*.dist-info'))
    if len(info_dirs) != 1:
        raise WheelToolsError("Should be exactly one `*.dist_info` directory")
    return info_dirs[0]


def _to_generic_pyver(pyver_tags):
    """Convert from CPython implementation to generic python version tags

    Convert each CPython version tag to the equivalent generic tag.

    For example::

        cp35 -> py3
        cp27 -> py2

    See https://www.python.org/dev/peps/pep-0425/#python-tag
    """
    return ['py%s' % tag[2] if tag.startswith('cp') else tag for tag in pyver_tags]


def _convert_to_generic_platform_wheel(wheel_ctx):
    """Switch to generic python tags and remove ABI tags from a wheel

    Convert implementation specific python tags to their generic equivalent and
    remove all ABI tags from wheel_ctx's filename and ``WHEEL`` file.

    Parameters
    ----------
    wheel_ctx : InWheelCtx
        An open wheel context
    """

    abi_tags = ['none']

    info_fname = pjoin(_dist_info_dir(wheel_ctx.wheel_path), 'WHEEL')
    info = read_pkg_info(info_fname)

    # Check what tags we have
    if wheel_ctx.out_wheel is not None:
        out_dir = dirname(wheel_ctx.out_wheel)
        wheel_fname = basename(wheel_ctx.out_wheel)
    else:
        out_dir = '.'
        wheel_fname = basename(wheel_ctx.in_wheel)

    # Update wheel filename
    parsed_fname = WHEEL_INFO_RE(wheel_fname)
    fparts = parsed_fname.groupdict()
    original_platform_tags = fparts['plat'].split('.')

    original_abi_tags = fparts['abi'].split('.')
    logger.debug('Previous ABI tags: %s', ', '.join(original_abi_tags))
    if abi_tags != original_abi_tags:
        logger.debug('New ABI tags ....: %s', ', '.join(abi_tags))
        fparts['abi'] = '.'.join(abi_tags)
    else:
        logger.debug('No ABI tags change needed.')

    original_pyver_tags = fparts['pyver'].split('.')
    logger.debug('Previous pyver tags: %s', ', '.join(original_pyver_tags))
    pyver_tags = _to_generic_pyver(original_pyver_tags)
    if pyver_tags != original_pyver_tags:
        logger.debug('New pyver tags ....: %s', ', '.join(pyver_tags))
        fparts['pyver'] = '.'.join(pyver_tags)
    else:
        logger.debug('No pyver change needed.')

    _, ext = splitext(wheel_fname)
    fparts['ext'] = ext
    out_wheel_fname = "{namever}-{pyver}-{abi}-{plat}{ext}".format(**fparts)

    logger.info('Previous filename: %s', wheel_fname)
    if out_wheel_fname != wheel_fname:
        logger.info('New filename ....: %s', out_wheel_fname)
    else:
        logger.info('No filename change needed.')

    out_wheel = pjoin(out_dir, out_wheel_fname)

    # Update wheel tags
    in_info_tags = [tag for name, tag in info.items() if name == 'Tag']
    logger.info('Previous WHEEL info tags: %s', ', '.join(in_info_tags))

    # Python version, C-API version combinations
    pyc_apis = []
    for tag in in_info_tags:
        py_ver = '.'.join(_to_generic_pyver(tag.split('-')[0].split('.')))
        abi = 'none'
        pyc_apis.append('-'.join([py_ver, abi]))
    # unique Python version, C-API version combinations
    pyc_apis = unique_by_index(pyc_apis)

    # Set tags for each Python version, C-API combination
    updated_tags = ['-'.join(tup) for tup in product(pyc_apis, original_platform_tags)]

    if updated_tags != in_info_tags:
        del info['Tag']
        for tag in updated_tags:
            info.add_header('Tag', tag)

        logger.info('New WHEEL info tags ....: %s', ', '.join(info.get_all('Tag')))
        write_pkg_info(info_fname, info)
    else:
        logger.info('No WHEEL info change needed.')
    return out_wheel


def convert_to_generic_platform_wheel(wheel_path, out_dir='./dist/', remove_original=False, verbose=0):
    logging.disable(logging.NOTSET)
    if verbose >= 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    wheel_fname = basename(wheel_path)
    out_dir = abspath(out_dir)

    with InWheelCtx(wheel_path) as ctx:
        ctx.out_wheel = pjoin(out_dir, wheel_fname)
        ctx.out_wheel = _convert_to_generic_platform_wheel(ctx)

    if remove_original:
        logger.info('Removed original wheel %s' % wheel_path)
        os.remove(wheel_path)


def main():
    p = argparse.ArgumentParser(description='Convert wheel to be independent of python implementation and ABI')
    p.set_defaults(prog=basename(sys.argv[0]))
    p.add_argument("-v",
                   "--verbose",
                   action='count',
                   dest='verbose',
                   default=0,
                   help='Give more output. Option is additive')

    p.add_argument('WHEEL_FILE', help='Path to wheel file.')
    p.add_argument('-w',
                   '--wheel-dir',
                   dest='WHEEL_DIR',
                   type=abspath,
                   help='Directory to store updated wheels (default: "dist/")',
                   default='dist/')
    p.add_argument("-r",
                   "--remove-original",
                   dest='remove_original',
                   action='store_true',
                   help='Remove original wheel')

    args = p.parse_args()

    if not isfile(args.WHEEL_FILE):
        p.error('cannot access %s. No such file' % args.WHEEL_FILE)

    convert_to_generic_platform_wheel(args.WHEEL_FILE, args.WHEEL_DIR, args.remove_original, args.verbose)


if __name__ == '__main__':
    main()
