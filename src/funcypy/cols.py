'Operating on collections'

import functools
from typing import Callable, Generator
from . funcy import complement

missing = object()

def keymap(oper: Callable, obj: dict=missing) -> Generator:
    'Perform a map operation over the keys of a dict'
    if obj is missing: return functools.partial(keymap, oper)
    for k, v in obj.items():
        yield oper(k), v

def valmap(oper: Callable, obj: dict=missing) -> Generator:
    'Perform a map operation over the values of a dict'
    if obj is missing: return functools.partial(valmap, oper)
    for k, v in obj.items():
        yield k, oper(v)

def itemmap(oper: Callable, obj: dict=missing) -> Generator:
    'Perform a map operation over the items of a dict'
    if obj is missing: return functools.partial(itemmap, oper)
    for k, v in obj.items():
        yield oper(k, v)

def keyfilter(oper: Callable, obj: dict=missing) -> Generator:
    if obj is missing: return functools.partial(keyfilter, oper)
    for k, v in obj.items():
        if oper(k): yield k, v

def valfilter(oper: Callable, obj: dict=missing) -> Generator:
    if obj is missing: return functools.partial(valfilter, oper)
    for k, v in obj.items():
        if oper(v): yield k, v

def removekey(oper: Callable, obj: dict=missing) -> Generator:
    return keyfilter(complement(oper), obj)

def removeval(oper: Callable, obj: dict=missing) -> Generator:
    return valfilter(complement(oper), obj)

def field_filter(fields, obj=missing):
    'filter for the specified fields from the obj'
    if obj is missing: return functools.partial(field_filter, fields)
    return keyfilter(
        lambda k: k in fields,
        # dict(zip(fields, toolz.get(fields, obj, default=missing)))
    )


def flatten(obj: dict, _name_space=""):
    """Takes a nested dict and flattens the values:
        flatten({"some": {"nested": {"value1": 1, "value2": 2}, "other": 3}})
    returns:
        {"some.nested.value1": 1, "some.nested.value2": 2, "some.other": 3}
    """
    for key, val in obj.items():
        k = ".".join([_name_space, key])
        if isinstance(val, dict):
            for kk, vv in flatten(val, k):
                yield kk, vv
        else:
            yield k[1:], val
