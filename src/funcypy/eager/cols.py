'Operating on collections'

import functools
from typing import Callable, List, Union
from .. import cols
from .. funcy import partial


@partial
def keymap(oper: Callable, obj: dict) -> dict:
    return dict(cols.keymap(oper, obj))

@partial
def valmap(oper: Callable, obj: dict) -> dict:
    return dict(cols.valmap(oper, obj))

@partial
def itemmap(oper: Callable, obj: dict) -> dict:
    return dict(cols.itemmap(oper, obj))

@partial
def keyfilter(oper: Union[Callable, str, List[str]], obj: dict) -> dict:
    return dict(cols.keyfilter(oper, obj))

@partial
def valfilter(oper: Callable, obj: dict) -> dict:
    return dict(cols.valfilter(oper, obj))

@partial
def removekey(oper: Union[Callable, str, List[str]], obj: dict) -> dict:
    return dict(cols.removekey(oper, obj))

@partial
def removeval(oper: Callable, obj: dict) -> dict:
    return dict(cols.removeval(oper, obj))

def removevalnone(obj: dict) -> dict:
    return dict(cols.removevalnone(obj))

@partial
def field_filter(fields: List[str], obj: dict):
    return dict(cols.field_filter(fields, obj))

def flatten(obj: dict, _name_space: str="", depth: int=-1, follow_list: bool=False) -> dict:
    return dict(cols.flatten(obj, _name_space=_name_space, depth=depth, follow_list=follow_list))

def nestten(obj: dict) -> dict:
    return dict(cols.nestten(obj.items()))
