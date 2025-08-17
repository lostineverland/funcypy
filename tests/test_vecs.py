'Test vecs operators module'

import pytest
from funcypy import vecs, maps


def test_concat():
    assert vecs.concat()(3) == [3]
    assert vecs.concat(3, 4) == [3, 4]
    assert vecs.concat([3, 4], [5, 6]) == [3, 4, 5, 6]
    assert vecs.concat(3, 4, [5, 6]) == [3, 4, 5, 6]

def test_map():
    add_1 = lambda x: x + 1
    val = vecs.map(maps.valmap(add_1))([{'x': i} for i in range(3)])
    assert val == [{'x': i} for i in range(1, 4)]