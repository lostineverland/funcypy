'A module for set operations'

from typing import Callable, Tuple
from funcypy.seqs import concat
from funcypy.types import is_iterable

def superset(*items: Tuple) -> Callable:
    """Given a collection it returns the `superset` function of a set
        wrapped in a more useful form, such that:
        superset('some', 1, 'me')('some') == True
        superset('some', 1, 'me')(1, me) == True
        superset('some', 1, 'me')('some', 'other') == False
    """
    # assert not any(isinstance(i, (list, dict, tuple, set)) for i in items), "Iterable (list?, dict?) is nested in items"
    if len(items) == 1 and not isinstance(items[0], str):
        items = list(concat(*items))
    else:
        items = list(concat(items))
    def f(*args):
        if len(args) == 1 and not isinstance(args[0], str):
            return set(items).issuperset(list(concat(args)))
        else:
            return set(items).issuperset(args)
    return f

has = superset
contains = superset

def subset(*items: Tuple) -> Callable:
    """Given a collection it returns the `subset` function of a set
        wrapped in a more useful form, such that:
        subset('some')('some', 1, 'me') == True
        subset(1, 'me')('some', 1, 'me') == True
        subset('some', 'other')('some', 1, 'me') == False
    """
    return lambda *i: set(items).issubset(i)

all_of = subset

def intersect(*items: Tuple) -> Callable:
    """Given a collection it returns the `intersect` function of a set
        wrapped in a more useful form, such that:
        intersect('some')('some', 1, 'me') == ['some']
        intersect(1, 'me')('some', 1, 'me') == [1, 'me']
        intersect('some', 'other')('some', 1, 'me') == ['some']
      * order is consistent but not so predictable
    """
    return lambda *i: list(set(items).intersection(i))

any_of = intersect

