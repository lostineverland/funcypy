'Test seqs operators module'

import pytest
from funcypy.funcy import *

@partial(count=1)
def add(x, y):
    return x + y

@partial(1)
def pow(y, x):
    return x ** y

def test_partial():
    assert add(2, 3) == 5

def test_rcomp_complement():
    assert rcomp(add(3), pow(2))(2) == 25
    assert complement(rcomp(add(3), pow(2)))(2) == False

def test_pipe():
    assert pipe(2, add(3), pow(2)) == 25

def test_superset():
    assert superset('some', 1, 'me')('some')
    assert superset('some', 1, 'me')(1, 'me')
    assert not superset('some', 1, 'me')('some', 'other')
    assert has(3, 4, 5)(3)

def test_subset():
    assert subset('some')('some', 1, 'me')
    assert subset(1, 'me')('some', 1, 'me')
    assert not subset('some', 'other')('some', 1, 'me')

def test_intersect():
    assert set(intersect('some')('some', 1, 'me')) == set(['some'])
    assert set(intersect(1, 'me')('some', 1, 'me')) == set(['me', 1])
    assert set(intersect('some', 'other')('some', 1, 'me')) == set(['some'])

def test_juxt():
    assert juxt(subset(3, 4, 5), intersect(3, 4, 5), superset(3, 4, 5))(3, 5) == [False, [3, 5], True]

def test_pmap():
    assert list(pmap(add(3))(range(5))) == list(map(add(3), range(5)))
    assert list(pmap([add(3), add(1)])(range(5))) == list(map(add(4), range(5)))
