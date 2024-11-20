'Operating on collections'

import functools
from typing import Callable, Generator, Tuple, Iterable, Iterator, Any, Union
from . funcy import complement, has, partial
from . seqs import concat, iterator


HashCol = Union[dict, Iterable[Tuple[str, Any]]]
Missing = object
HashColOrMissing = Union[HashCol, Missing]

missing: Missing= object()

@partial
def keymap(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a map operation over the keys of a dict'
    if isinstance(mseq, dict): mseq = mseq.items()
    for k, v in mseq:
        yield oper(k), v

@partial
def valmap(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a map operation over the values of a dict'
    if isinstance(mseq, dict): mseq = mseq.items()
    for k, v in mseq:
        yield k, oper(v)

@partial
def itemmap(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a map operation over the items of a dict'
    if isinstance(mseq, dict): mseq = mseq.items()
    for k, v in mseq:
        yield oper(k, v)

@partial
def keyfilter(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a filter operation over the keys of a dict'
    if isinstance(mseq, dict): mseq = mseq.items()
    for k, v in mseq:
        if oper(k): yield k, v

@partial
def valfilter(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a filter operation over the vals of a dict'
    if isinstance(mseq, dict): mseq = mseq.items()
    for k, v in mseq:
        if oper(v): yield k, v

@partial
def removekey(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a remove operation over the keys of a dict'
    return keyfilter(complement(oper), mseq)

@partial
def removeval(oper: Callable, mseq: HashCol) -> Generator:
    'Perform a remove operation over the vals of a dict'
    return valfilter(complement(oper), mseq)

@partial
def field_filter(fields: Tuple, mseq: HashCol) -> Generator:
    'apply a white list filter (fields) to the dict keys'
    return keyfilter(
        has(*fields),
        mseq
    )

def flatten(mseq: HashCol, _name_space: str="", depth: int=-1, follow_list: bool=False, all_possible_keys=False) -> Generator:
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
    if isinstance(mseq, dict): mseq = mseq.items()
    for key, val in mseq:
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

def nestten(key_val: Iterable, base: str='') -> Generator[Tuple[str, Any], Tuple[str, Any], None]:
    '''This is the complement of flatten, such that:
        dict(nestten(flatten(val, follow_list=True))) == val
    '''
    if not base: key_val = iterator(key_val)
    keys, val = next(key_val, (None, None))
    while keys:
        k = keys
        if base:
            k = keys.replace(base + '.', '', 1)
            if base not in keys:
                key_val.send([keys, val])
                break
        if len(b_k := k.split('.', 1)) > 1:
            key, rest_keys = b_k
            kk_vv = key_val.send([keys, val])
            vals = dict(nestten(
                key_val,
                base='.'.join(filter(None, [base, key])),
                ))
            if all(map(str.isnumeric, vals.keys())): vals = list(vals.values())
            yield key, vals
        else:
            key = b_k[0]
            yield key, val
        keys, val = next(key_val, (None, None))
