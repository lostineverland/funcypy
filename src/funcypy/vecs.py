'Operating on sequences'

import functools
from typing import List, Iterable, Callable, Dict, Union
from funcypy.funcy import partial, map, rcomp
from funcypy import seqs


@partial
def concat(*seq: Iterable) -> List:
    return list(seqs.concat(*seq))

def map(*func: Callable, monitor: Union[bool, Dict]=True) -> Callable:
    "A curried and composable (rcomp) map function"
    vmap = lambda f, items: [f(i) for i in items]
    return functools.update_wrapper(
        functools.partial(vmap, rcomp(*func, monitor=monitor)),
        map)
