'tools to handle lazy objects (sequences)'

import functools
from typing import Generator, Iterable, Iterator, List, Tuple, Any, Union

missing = object()

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

def concat(*seqs: Tuple[Iterable]) -> Iterable:
    'concatenate sequences'
    for seq in seqs:
        for i in seq:
            yield i

def iterator(seq: Iterable) -> Generator:
    'An iterator which allows a rewind'
    if not isinstance(seq, Iterator): seq = iter(seq)
    i = next(seq, missing)
    while i is not missing:
        rewind = yield i
        while rewind:              # the send() method actually triggers the yield,
            yield                  # so this yield returns None to the send statement
            rewind = yield rewind  # which triggered the rewind
        else:
            i = next(seq, missing)

