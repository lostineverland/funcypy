'tools to handle lazy objects (sequences)'

import functools, itertools
from typing import Generator, Iterable, Iterator, List, Tuple, Any, Union, Callable
from collections.abc import Iterable as IterableType
missing = object()
skip = object()
cont = object()

def is_lazy(obj: Any) -> bool:
    isLazy = lambda e: hasattr(obj, e)
    return all(hasattr(obj, i) for i in ['__next__', '__iter__'])

def is_iterable(obj: Any) -> bool:
    return isinstance(obj, IterableType)

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
