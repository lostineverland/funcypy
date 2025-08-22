'This module deals with type checking'

from typing import Generator, Iterable, Iterator, List, Tuple, Any
from collections.abc import Iterable as IterableType

def is_lazy(obj: Any) -> bool:
    isLazy = lambda e: hasattr(obj, e)
    return all(hasattr(obj, i) for i in ['__next__', '__iter__'])

def is_iterable(obj: Any) -> bool:
    return isinstance(obj, IterableType)

