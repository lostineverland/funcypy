'Test seqs operators module'

import pytest
from funcypy.funcy import *

@partial
def add(x, y):
    return x + y

@partial
def pow(y, x):
    return x ** y

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