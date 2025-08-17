'Test sess operators module'

import pytest
from funcypy.sets import *

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

