'tools to handle lazy objects (sequences)'

import functools
missing = object()

def take(n, seq=missing):
    if seq is missing: return functools.partial(take, n)
    vals = []
    for i in range(n):
        try:
            vals += [next(seq)]
        except StopIteration:
            return vals
    return vals

def limit_seq(limit, seq=missing):
    '''allows you to set a hard limit on a sequence
    '''
    if seq is missing: return functools.partial(limit_seq, limit)
    for i, val in enumerate(seq):
        if i == limit: break
        yield val

def loop(val):
    if isinstance(val, list):
        while True:
            for i in val:
                yield i
    while True:
        yield val

def nth(n, seq=missing):
    if seq is missing: return functools.partial(nth, n)
    N = n - 1
    for i, x in enumerate(seq):
        if i == N: break
    if i < N:
        return None
    else:
        return x

def last(seq):
    for i in seq:
        val = i
    return val

def concat(*seqs):
    'concatenate sequences'
    for seq in seqs:
        for i in seq:
            yield i
