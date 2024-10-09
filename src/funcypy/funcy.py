'Operating on functions'

import functools
from typing import Callable, Union, Generator

missing = object()

def complement(func: Callable) -> Callable:
    'Return the complement of a function (the boolean opposite)'
    @functools.wraps(func)
    def f(*args, **kwargs):
        return not func(*args, **kwargs)
    return f

def rcomp(*funcs: Callable) -> Callable:
    'reverse function composition'
    return lambda y: functools.reduce(lambda x, f: f(x), funcs, y)

def keymap(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    'Perform a map operation over the keys of a dict'
    if obj is missing:
        if lazy == False: return functools.partial(keymap, oper)
        return functools.partial(keymap, oper, lazy=True)
    if lazy:
        for k, v in obj.items():
            yield oper(k), v
    else:
        return dict(keymap(oper, obj, lazy=True))

def valmap(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    'Perform a map operation over the values of a dict'
    if obj is missing:
        if lazy == False: return functools.partial(valmap, oper)
        return functools.partial(valmap, oper, lazy=True)
    if lazy:
        for k, v in obj.items():
            yield k, oper(v)
    else:
        return dict(valmap(oper, obj, lazy=True))

def itemmap(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    'Perform a map operation over the items of a dict'
    if obj is missing:
        if lazy == False: return functools.partial(itemmap, oper)
        return functools.partial(itemmap, oper, lazy=True)
    if lazy:
        for k, v in obj.items():
            yield oper(k, v)
    else:
        return dict(itemmap(oper, obj, lazy=True))

def keyfilter(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    if obj is missing:
        if lazy == False: return functools.partial(keyfilter, oper)
        return functools.partial(keyfilter, oper, lazy=True)
    if lazy:
        for k, v in obj.items():
            if oper(k): yield k, v
    else:
        return dict(keyfilter(oper, obj, lazy=True))

def valfilter(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    if obj is missing:
        if lazy == False: return functools.partial(valfilter, oper)
        return functools.partial(valfilter, oper, lazy=True)
    if lazy:
        for k, v in obj.items():
            if oper(v): yield k, v
    else:
        return dict(valfilter(oper, obj, lazy=True))

def removekey(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    return keyfilter(complement(oper), obj, lazy)

def removeval(oper: Callable, obj: dict=missing, lazy=False) -> Union[dict, Generator]:
    return valfilter(complement(oper), obj, lazy)

def field_filter(fields, obj=missing):
    'filter for the specified fields from the obj'
    if obj is missing: return functools.partial(field_filter, fields)
    return keyfilter(
        lambda k: k in fields,
        # dict(zip(fields, toolz.get(fields, obj, default=missing)))
    )

def partial(func):
    '''The functtools.partial function as a decorator, it works very much like the 
        @curry decorator, except it always returns a function which will
        execute the next time it is called (regardless if there are missing
        arguments)
    '''
    @functools.wraps(func)
    def f(*args, **kwargs):
        return functools.partial(func, *args, **kwargs)
    return f

def flatten(obj: dict, _name_space="", lazy=False):
    """Takes a nested dict and flattens the values. The function returns an iterator
    of the dict items. Such that:
        dict(flatten({"some": {"nested": {"value1": 1, "value2": 2}, "other": 3}}))
    returns:
        {"some.nested.value1": 1, "some.nested.value2": 2, "some.other": 3}
    """
    if not lazy: return dict(flatten(obj, lazy=True))
    for key, val in obj.items():
        k = ".".join([_name_space, key])
        if isinstance(val, dict):
            for kk, vv in flatten(val, k, lazy):
                yield kk, vv
        else:
            yield k[1:], val
