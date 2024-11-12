'Operating on functions'

import functools
from typing import Any, Callable, Tuple


def complement(func: Callable) -> Callable:
    'Return the complement of a function (the boolean opposite)'
    @functools.wraps(func)
    def f(*args, **kwargs):
        return not func(*args, **kwargs)
    return f

def rcomp(*funcs: Callable) -> Callable:
    'reverse function composition'
    return lambda y: functools.reduce(lambda x, f: f(x), funcs, y)

def partial(func: Callable) -> Callable:
    '''The functtools.partial function as a decorator, it works very much like the 
        @curry decorator, except it always returns a function which will
        execute the next time it is called (regardless if there are missing
        arguments)
    '''
    @functools.wraps(func)
    def f(*args, **kwargs):
        return functools.partial(func, *args, **kwargs)
    return f

def pipe(*args: Tuple[Any, Callable]):
    "run an input through a list of functions"
    y = args[0]
    funcs = args[1:]
    return functools.reduce(lambda x, f: f(x), funcs, y)

def once(func):
    '''A decorator which ensures that `func` is only run once.
        It caches the results of the single execution and returns
        them on any subsequent call regardless of changes to the
        function arguments
    '''
    c = 0
    res = []
    @functools.wraps(func)
    def f(*args, **kwargs):
        nonlocal c
        if c == 0:
            c += 1
            res.append(func(*args, **kwargs))
        return res[0]
    return f
