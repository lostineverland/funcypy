'Operating on sequences'

import functools, itertools
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

@partial
def groupby(oper: Union[Callable, str], mseq: List[Dict]) -> Dict:
    if isinstance(oper, str):
        op = lambda e: e.get(oper)
    else:
        op = oper
    return {k: list(v) for k, v in itertools.groupby(sorted(mseq, key=op), key=op)}

