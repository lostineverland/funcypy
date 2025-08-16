'Test curry module'

import pytest
from funcypy import curry

def test_func():
    assert curry.func.reduce(lambda mem, i: mem + i)(range(3)) == 3
    assert curry.func.reduce(lambda mem, i: mem + i)(range(3), 10) == 13

def test_iter():
    odd = lambda x: x % 2
    coll = sorted(range(10), key=odd)
    assert {k: list(v) for k,v in curry.iter.groupby(key=odd)(coll)} == {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}

