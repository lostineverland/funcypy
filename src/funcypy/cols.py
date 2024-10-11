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
    'Perform a filter operation over the keys of a dict'
    if obj is missing: return functools.partial(keyfilter, oper)
    for k, v in obj.items():
        if oper(k): yield k, v

def valfilter(oper: Callable, obj: dict=missing) -> Generator:
    'Perform a filter operation over the vals of a dict'
    if obj is missing: return functools.partial(valfilter, oper)
    for k, v in obj.items():
        if oper(v): yield k, v

def removekey(oper: Callable, obj: dict=missing) -> Generator:
    'Perform a remove operation over the keys of a dict'
    return keyfilter(complement(oper), obj)

def removeval(oper: Callable, obj: dict=missing) -> Generator:
    'Perform a remove operation over the vals of a dict'
    return valfilter(complement(oper), obj)

def field_filter(fields: list, obj: dict=missing) -> dict:
    'apply a white list filter (fields) to the dict keys'
    if obj is missing: return functools.partial(field_filter, fields)
    return keyfilter(
        lambda k: k in fields,
        obj
    )

def flatten(obj: dict, _name_space="") -> dict:
    """Takes a nested dict and flattens the values such that:
    {
        "some": {
            "nested": {
                "value1": 1, 
                "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, 
            "other": 3}}
    is transformed into:
    {
        "some.nested.value1": 1, 
        "some.nested.value2": [{"more":{"nesting": 3}}, {"value4": 4}], 
        "some.other": 3}

    but perhaps we want further depth?: (not implemented)
        "some.nested.value2": [
                                {"more.nesting": 3}, 
                                {"value4": 4}], 
    or:
        "some.nested.value2".[0].more.nesting": 3}, 
        "some.nested.value2".[1].value4": 4, 
    """
    for key, val in obj.items():
        k = ".".join([_name_space, key])
        if isinstance(val, dict):
            for kk, vv in flatten(val, k):
                yield kk, vv
        else:
            yield k[1:], val
