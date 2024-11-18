'Operating on collections'

import functools
from typing import Callable, Generator, Tuple, Iterable, Iterator, Any, Union
from . funcy import complement, log
from . seqs import concat

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

def flatten(obj: dict, _name_space: str="", depth: int=-1, follow_list: bool=False, all_possible_keys=False) -> Generator:
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

def expand_(key_val: Iterable[Tuple[str, Any]], mem=''):
    col = []
    for key, val in key_val:
        if len(ks := key.split('.', 1)) > 1:
            base, k = ks
            if base == mem:
                col += [(k, val)]
            else:
                yield mem, expand_(col, base)
                col = [(k, val)]
        else:
            kk, vv = col[0]
            if kk.isnumeric():
                yield key, [vv for kk, vv in col] 
            else:
                yield key, {kk: vv for kk, vv in col}
            col = [(k, val)]

def expand(key_val: dict, base: str = ''):
    return dict(collect(key_val))
    # return nesten(key_val)

def iterator(key_val):
    if isinstance(key_val, dict):
        key_val = key_val.items()
    for k_v in key_val:
        log(yields=k_v)
        prev = yield k_v
        if prev:
    # this mechanism is not working
    #  I should try to use a while loop with next
    #  the problem is that rewinding takes an extra
    #  step, which acts like it is skipping
            log(yield_k_v=k_v)
            yield k_v
            log(yield_prev=prev)
            yield prev
            
def collect(key_val: Union[Iterator, dict], base: str='', nesting: int=50) -> Generator[Tuple[str, Any], Tuple[str, Any], None]:
    if not base: key_val = iterator(key_val)
    keys, val = next(key_val, (None, None))
    log(where='begin', received=[keys, val])
    while keys:
        k = keys
        if base:
            k = keys.replace(base + '.', '', 1)
            if base not in keys:
                key_val.send([keys, val])
                log('break', send=[keys, val])
                break
        if len(b_k := k.split('.', 1)) > 1:
            key, rest_keys = b_k
            log(nesting=nesting, base=base, keys=keys, b_k=k.split('.', 1), key=key, val=val, k=k, n_base='.'.join(filter(None, [base, key])))
            key_val.send([keys, val])
            log('new_func', send=[keys, val])
            vals = dict(collect(
                key_val,
                base='.'.join(filter(None, [base, key])),
                nesting=nesting - 1,
                ))
            if all(map(str.isnumeric, vals.keys())): vals = list(vals.values())
            yield key, vals
        else:
            key = b_k[0]
            log(nesting=nesting, base=base, keys=keys, b_k=b_k[0], key=key, val=val, k=k)
            yield key, val
        keys, val = next(key_val, (None, None))
        log(where='end', received=[keys, val])

def nesten(key_val: Union[Iterator, dict]) -> dict:
    if isinstance(key_val, dict): key_val = iter(key_val.items())
    nested_dict = {}
    for flat_key, value in key_val:
        keys = flat_key.split(".")
        current_level = nested_dict
        
        for i, key in enumerate(keys[:-1]):
            # Check if the key is a digit indicating a list index
            if key.isdigit():
                key = int(key)
                if not isinstance(current_level, list):
                    # Initialize a list if it's not already a list
                    current_level = []
                while len(current_level) <= key:
                    current_level.append({})
                current_level = current_level[key]
            else:
                if key not in current_level:
                    next_key = keys[i + 1]
                    # Initialize a list if the next key is a digit
                    current_level[key] = [] if next_key.isdigit() else {}
                current_level = current_level[key]
        
        last_key = keys[-1]
        if last_key.isdigit():
            last_key = int(last_key)
            if not isinstance(current_level, list):
                current_level = []
            while len(current_level) <= last_key:
                current_level.append(None)
            current_level[last_key] = value
        else:
            current_level[last_key] = value

    return nested_dict

