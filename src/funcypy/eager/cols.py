'Operating on collections'

import functools
from typing import Callable
from .. import cols

missing = object()

def keymap(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(keymap, oper)
    return dict(cols.keymap(oper, obj))

def valmap(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(valmap, oper)
    return dict(cols.valmap(oper, obj))

def itemmap(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(itemmap, oper)
    return dict(cols.itemmap(oper, obj))

def keyfilter(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(keyfilter, oper)
    return dict(cols.keyfilter(oper, obj))

def valfilter(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(valfilter, oper)
    return dict(cols.valfilter(oper, obj))

def removekey(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(removekey, oper)
    return dict(cols.removekey(oper, obj))

def removeval(oper: Callable, obj: dict=missing) -> dict:
    if obj is missing: return functools.partial(removeval, oper)
    return dict(cols.removeval(oper, obj))

def field_filter(fields, obj=missing):
    if obj is missing: return functools.partial(field_filter, fields)
    return dict(cols.field_filter(fields, obj))

def flatten(obj: dict, _name_space: str="", depth: int=-1, follow_list: bool=False) -> dict:
    return dict(cols.flatten(obj, _name_space=_name_space, depth=depth, follow_list=follow_list))
