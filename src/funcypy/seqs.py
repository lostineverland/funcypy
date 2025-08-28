'tools to handle lazy objects (sequences)'

import functools, itertools
from typing import Generator, Iterable, Iterator, List, Tuple, Any, Union, Callable
from funcypy.funcy import partial, rcomp, some
from funcypy.types import is_lazy, is_iterable
missing = object()
skip = object()
cont = object()

def take(n: int, seq: Iterable=missing) -> List:
    if seq is missing: return functools.partial(take, n)
    vals = []
    for i in range(n):
        try:
            vals += [next(seq)]
        except StopIteration:
            return vals
    return vals

def limit_seq(limit: int, seq: Iterable) -> Generator:
    '''allows you to set a hard limit on a sequence
    '''
    for i, val in enumerate(seq):
        if i == limit: break
        yield val

def loop(val: Union[Any, List]) -> Generator:
    '''Create an infinite loop of val, if val is a list it will
         be infinitely replayed
    '''
    if isinstance(val, list):
        while True:
            for i in val:
                yield i
    while True:
        yield val

def nth(n: int, seq: Iterable=missing) -> Union[Any, None]:
    if seq is missing: return functools.partial(nth, n)
    N = n - 1
    for i, x in enumerate(seq):
        if i == N: break
    if i < N:
        return None
    else:
        return x

def last(seq: Iterable) -> Union[Any, None]:
    val = None
    for i in seq:
        val = i
    return val

def concat(*seq: Tuple[Iterable]) -> Generator:
    'concatenate sequences'
    for col in seq:
        if isinstance(col, Iterable):
            for i in col:
                yield i
        else:
            yield col

# def concat(*seq: Tuple[Iterable]) -> Generator:
#     'concatenate sequences'
#     for col in seq:
#         # print('col:', col)
#         if isinstance(col, Iterable):
#             for i in col:
#                 # print('i:', i)
#                 if isinstance(i, Iterable):
#                     for j in concat(*i):
#                         # print('j:', j)
#                         yield j
#                 else:
#                     yield i
#         else:
#             yield col

def iterator(seq: Iterable) -> Generator:
    '''An iterator which allows a "rewind" in the form of value re-insertion
        eg:
        items = iterator([2, 3, 5])
        next(items)   # 2
        next(items)   # 3
        items.send(4) # None
        next(items)   # 4
        next(items)   # 5
    '''
    if not isinstance(seq, Iterator): seq = iter(seq)
    i = next(seq, missing)
    while i is not missing:
        rewind = yield i
        while rewind:              # the send() method actually triggers the yield,
            yield                  # so this yield returns None to the send statement
            rewind = yield rewind  # which triggered the rewind
        else:
            i = next(seq, missing)
# @partial
# def map(func: Union[Callable, List[Callable]], seq: Iterable) -> Generator:
#     'Your friendly neighborhood map, but composable and curried'
#     f = funcy.rcomp(func)
#     if isinstance(func, list): func = rcomp(*func)
#     i = next(seq, missing)
#     while i is not missing:
#         val = f(i)
#         if val != skip:
#             yield val
#         i = next(seq, missing)

@partial
def select(pred: Union[Callable, List[Callable]], item: Any) -> Union[Any, None]:
    'A simple selector based on a truthy predicate'
    if not isinstance(pred, list): pred = [pred]
    pred = some(*pred)
    if pred(item): return item

@partial(count=2)
def cond(pred: Union[Callable, List[Callable]], func: Union[Callable, List[Callable]], seq: Iterable=missing) -> Generator:
    '''Like a conditional map with filter, such that `func` is only applied if the pred results is True (truthy values don't work here).
        Otherwise it will return the unchanged value. Falsy values are not sufficient other than None.
        For truthy values use `select` as the predicate
    '''
    if not is_iterable(pred): pred = [pred]
    if not is_iterable(func): func = [func]
    if not is_lazy(seq): seq = iter(seq)
    pred = some(*pred)
    func = rcomp(*func)
    i = next(seq, missing)
    while i is not missing:
        sel = pred(i)
        if sel is True:
            yield func(i)
        else:
            yield i
        i = next(seq, missing)
