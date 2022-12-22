# -*- coding: utf-8 -*-
import sys
from contextlib import contextmanager


@contextmanager
def push_argv(argv):
    old_argv = sys.argv
    sys.argv = argv
    yield
    sys.argv = old_argv
