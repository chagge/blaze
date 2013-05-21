from __future__ import absolute_import

# build the blaze namespace with selected functions

from . import datashape, ckernel
from .datashape import dshape
from .array import Array
from .constructors import array, ones, zeros
from .persistence import load, save, open, drop, create, create_fromiter
__version__ = '0.0.1'

def print_versions():
    """Print all the versions of software that Blaze relies on."""
    import sys, platform
    import numpy as np
    from . import blz
    print("-=" * 38)
    print("Blaze version: %s" % __version__)
    print("NumPy version: %s" % np.__version__)
    print("BLZ version: %s" % blz.__version__)
    print("Blosc version: %s (%s)" % blz.blosc_version())
    print("Python version: %s" % sys.version)
    (sysname, nodename, release, version, machine, processor) = \
        platform.uname()
    print("Platform: %s-%s-%s (%s)" % (sysname, release, machine, version))
    if sysname == "Linux":
        print("Linux dist: %s" % " ".join(platform.linux_distribution()[:-1]))
    if not processor:
        processor = "not recognized"
    print("Processor: %s" % processor)
    print("Byte-ordering: %s" % sys.byteorder)
    print("Detected cores: %s" % blz.detect_number_of_cores())
    print("-=" * 38)


def test(verbosity=1, xunitfile=None, exit=False):
    """
    Runs the full Blaze test suite, outputting
    the results of the tests to sys.stdout.

    This uses nose tests to discover which tests to
    run, and runs tests in any 'tests' subdirectory
    within the Blaze module.

    Parameters
    ----------
        Value 0 prints very little, 1 prints a little bit,
        and 2 prints the test names while testing.
    xunitfile : string, optional
        If provided, writes the test results to an xunit
        style xml file. This is useful for running the tests
        in a CI server such as Jenkins.
    exit : bool, optional
        If True, the function will call sys.exit with an
        error code after the tests are finished.
    """
    import nose
    import os
    import sys
    argv = ['nosetests', '--verbosity=%d' % verbosity]
    # Output an xunit file if requested
    if xunitfile:
        argv.extend(['--with-xunit', '--xunit-file=%s' % xunitfile])
    # Add all 'tests' subdirectories to the options
    rootdir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(rootdir):
        if 'tests' in dirs:
            testsdir = os.path.join(root, 'tests')
            argv.append(testsdir)
            print('Test dir: %s' % testsdir[len(rootdir)+1:])
    sys.stdout.flush()
    # print versions (handy when reporting problems)
    print_versions()
    # Ask nose to do its thing
    return nose.main(argv=argv, exit=exit)
