'A collection of curried functions from the standard library'

import functools
import itertools
from . funcy import partial


class Lib:
    """A module wrapper"""
    def __init__(self, lib):
        self.lib = lib
    def __getattr__(self, arg):
        return partial(getattr(self.lib, arg))

func = Lib(functools)
iter = Lib(itertools)

