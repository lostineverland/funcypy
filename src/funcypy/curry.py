'A collection of curried functions from the standard library'

import functools
import itertools
import builtins
from . funcy import partial


class Lib:
    """A module wrapper"""
    def __init__(self, lib):
        self.lib = lib
    def __getattr__(self, name):
        try:
            func = getattr(self.lib, name)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        # Check if the attribute is callable
        if callable(func):
            return functools.update_wrapper(
                lambda *args, **kwargs: functools.partial(func, *args, **kwargs),
                func)
        else:
            raise AttributeError(f"'{name}' is not a callable attribute in {self.lib.__name__}")

func = Lib(functools)
iter = Lib(itertools)
stdlib = Lib(builtins)