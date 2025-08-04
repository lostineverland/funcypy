'Operating on collections'

import functools
from typing import Callable, List, Union, Iterable, Any
from .. import cols
from .. funcy import partial
from .. import seqs


@partial
def filter(oper: Callable, obj: Iterable) -> list:
    return list(cols.filter(oper, obj))

@partial
def remove(oper: Callable, obj: Iterable) -> list:
    return list(cols.remove(oper, obj))

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
def field_filter(fields: List[str], obj: dict) -> dict:
    return dict(cols.field_filter(fields, obj))

@partial
def pluck(fields: Union[str, List[str]], item: Union[dict, List[dict]]) -> Union[Any, List[Any]]:
    '''return the values (and only the values) in a dict which match the given fields
         this version also handles a list of dictionaries
        pluck('x', [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}, {'x': 2, 'y': 4}])
        => [0, 1, 2]
        pluck(['x', 'y'])({'x': 2, 'y': 4})
        => [2, 4]
        pluck(['x', 'y'])([{'x': 0, 'y': 0}, {'x': 1, 'y': 1}, {'x': 2, 'y': 4}])
        => [[0, 0], [1, 1], [2, 4]]
    '''
    if isinstance(fields, str):
        op = next
    elif isinstance(fields, Iterable):
        op = list
    if isinstance(item, dict):
        return op(cols.pluck(fields, item))
    elif isinstance(item, Iterable):
        return [op(cols.pluck(fields, i)) for i in item]

def flatten(obj: dict, _name_space: str="", depth: int=-1, follow_list: bool=False) -> dict:
    return dict(cols.flatten(obj, _name_space=_name_space, depth=depth, follow_list=follow_list))

def nestten(obj: dict) -> dict:
    return dict(cols.nestten(obj.items()))
