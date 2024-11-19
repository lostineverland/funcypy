'Operating on functions'

import functools, json
from typing import Any, Callable, Tuple

def log(x=None, name='value', **kwargs):
    '''A logging function which returns the value (as opposed to print which returns `None`)
        but will also print a JSON `{value: x}` of the given value. It also allows for
        kwargs to be included in the JSON.
    '''
    if x:
        print(json.dumps({name: x, **kwargs}))
    else:
        print(json.dumps(kwargs))
    return log

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

def superset(*items: Tuple) -> Callable:
    """Given a collection it returns the `superset` function of a set
        wrapped in a more useful form, such that:
        superset('some', 1, 'me')('some') == True
        superset('some', 1, 'me')(1, me) == True
        superset('some', 1, 'me')('some', 'other') == False
    """
    return lambda *i: set(items).issuperset(i)

has = superset
contains = superset

def subset(*items: Tuple) -> Callable:
    """Given a collection it returns the `subset` function of a set
        wrapped in a more useful form, such that:
        subset('some')('some', 1, 'me') == True
        subset(1, 'me')('some', 1, 'me') == True
        subset('some', 'other')('some', 1, 'me') == False
    """
    return lambda *i: set(items).issubset(i)

all_of = subset

def intersect(*items: Tuple) -> Callable:
    """Given a collection it returns the `intersect` function of a set
        wrapped in a more useful form, such that:
        intersect('some')('some', 1, 'me') == ['some']
        intersect(1, 'me')('some', 1, 'me') == [1, 'me']
        intersect('some', 'other')('some', 1, 'me') == ['some']
      * order is consistent but not so predictable
    """
    return lambda *i: list(set(items).intersection(i))

any_of = intersect

def juxt(*funcs: Callable) -> Callable:
    'Juxtapose functions'
    return lambda *i: [f(*i) for f in funcs]

