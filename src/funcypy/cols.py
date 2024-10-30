'Operating on collections'

import functools
from typing import Callable, Generator, Tuple
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

def field_filter(fields: Tuple, obj: dict=missing) -> dict:
    'apply a white list filter (fields) to the dict keys'
    if obj is missing: return functools.partial(field_filter, fields)
    return keyfilter(
        lambda k: k in fields,
        obj
    )

def flatten(obj: dict, _name_space: str="", depth: int=-1, follow_list: bool=False, all_possible_keys=False) -> dict:
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

    if follow_list:
        "some.nested.value2": [
                                {"more.nesting": 3}, 
                                {"value4": 4}], 
    becomes:
        "some.nested.value2.0.more.nesting": 3, 
        "some.nested.value2.1.value4": 4,

    depth dictates how many dots are allowed:
        depth=1
            {"some.nested": {
                "value1": 1, 
                "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, 
            "some.other": 3}
        
        depth=2
            {"some.nested.value1": 1,
            "some.nested.value2": [{"more":{"nesting": 3}}, {"value4": 4}],
            "some.other": 3
        }
            # further depth here would also require `follow_list=True`

    `all_possible_keys` contains duplicate data and should only be used to explore
    the key space 
    """
    for key, val in obj.items():
        k = ".".join([_name_space, key])
        if isinstance(val, dict) and depth != 0:
            if all_possible_keys: yield k[1:], val
            for kk, vv in flatten(val, k, depth=depth - 1, follow_list=follow_list, all_possible_keys=all_possible_keys):
                yield kk, vv
        elif isinstance(val, list) and depth != 0 and follow_list:
            if all_possible_keys: yield k[1:], val
            for kk, vv in flatten(
                    {str(i): j for i, j in enumerate(val)},
                    k,
                    depth=depth - 1,
                    follow_list=follow_list,
                    all_possible_keys=all_possible_keys):
                yield kk, vv
        else:
            yield k[1:], val
