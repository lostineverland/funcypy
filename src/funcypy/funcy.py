'Operating on functions'

import functools
import json
import builtins
from typing import Any, Callable, Tuple, Dict, Union
from funcypy.monitor import track
missing = object()


def log(x=None, name='value', logger=print, **kwargs):
    '''A logging function which returns the value (as opposed to print which returns `None`)
        but will also print a JSON `{value: x}` of the given value. It also allows for
        kwargs to be included in the JSON.
    '''
    if x:
        logger(json.dumps({name: x, **kwargs}))
    else:
        logger(json.dumps(kwargs))
    return log

def complement(func: Callable) -> Callable:
    'Return the complement of a function (the boolean opposite)'
    @functools.wraps(func)
    def f(*args, **kwargs):
        return not func(*args, **kwargs)
    return f

def rcomp(*funcs: Callable, monitor: Union[bool, Dict]=True) -> Callable:
    '''reverse function composition
        the monitor option allows for tracking of the functions for debugging
        or with a frequency keyword (int or function) for random sampling
    '''
    if monitor:
        if isinstance(monitor, dict):
            opts = {'frequency': 1, **monitor}
            return lambda y: functools.reduce(lambda x, f: track(f, **opts)(x), funcs, y)
        return lambda y: functools.reduce(lambda x, f: track(f, frequency=0)(x), funcs, y)
    return lambda y: functools.reduce(lambda x, f: f(x), funcs, y)

def partial(func: Callable=missing, count: int=1) -> Callable:
    '''The functtools.partial function as a decorator with a count trigger,
        it works very much like the @curry decorator, except it will 
        either (depending on the argument count) run or return a function 
        which will execute the next time it is called (regardless if 
        there  are missing arguments).
    '''
    if func is missing: return functools.partial(partial, count=count)
    if not callable(func): return functools.partial(partial, count=func)
    @functools.wraps(func)
    def f(*args, **kwargs):
        if sum([len(args), len(kwargs)]) > count:
            return func(*args, **kwargs)
        return functools.update_wrapper(functools.partial(func, *args, **kwargs), func)
    return f

def pipe(*args: Tuple[Any, Callable], monitor: Union[bool, Dict]=True) -> Any:
    """run an input through a list of functions
        the monitor option allows for tracking of the functions for debugging
        or with a frequency keyword (int or function) for random sampling
    """
    y = args[0]
    funcs = args[1:]
    if monitor:
        if isinstance(monitor, dict):
            opts = {'frequency': 1, **monitor}
            return functools.reduce(lambda x, f: track(f, **opts)(x), funcs, y)
        return functools.reduce(lambda x, f: track(f, frequency=0)(x), funcs, y)
    return functools.reduce(lambda x, f: f(x), funcs, y)

def once(func: Callable) -> Callable:
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

def juxt(*funcs: Callable) -> Callable:
    'Juxtapose functions'
    return lambda *i: [f(*i) for f in funcs]

def map(*func: Callable, monitor: Union[bool, Dict]=True) -> Callable:
    "A curried and composable (rcomp) map function"
    return functools.update_wrapper(
        functools.partial(builtins.map, rcomp(*func, monitor=monitor)),
        map)

def filter(*func: Callable, monitor: Union[bool, Dict]=True) -> Callable:
    "A curried and composable (rcomp) filter function"
    return functools.update_wrapper(
        functools.partial(filter, rcomp(*func, monitor=monitor)),
        cfilter)

def remove(*func: Callable, monitor: Union[bool, Dict]=True) -> Callable:
    "A curried and composable (rcomp) filter function"
    return functools.update_wrapper(
        functools.partial(filter, complement(rcomp(*func, monitor=monitor))),
        cremove)
