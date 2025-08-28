'Test funcy operators module'

import pytest
from funcypy import funcy, sets, maps

@funcy.partial(count=1)
def add(x, y):
    return x + y

@funcy.partial(1)
def pow(y, x):
    return x ** y

def test_partial():
    assert add(2, 3) == 5

def test_rcomp_complement():
    assert funcy.rcomp(add(3), pow(2))(2) == 25
    assert funcy.rcomp(funcy.rcomp(add(3), add(3)), pow(2))(2) == 64
    assert funcy.complement(funcy.rcomp(add(3), pow(2)))(2) == False

def test_some():
    data = {"some": {"nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "other": 3}}
    assert funcy.some(
        maps.pluck('some'),
        maps.pluck('nested'),
        maps.pluck('value1'),
        )(data) == 1
    assert funcy.some(
        lambda x: x.get('someday'),
        lambda x: x.get('nested'),
        lambda x: x.get('value1'),
        )(data) == None

def test_pipe():
    assert funcy.pipe(2, add(3), pow(2)) == 25

def test_juxt():
    assert funcy.juxt(sets.subset(3, 4, 5), sets.intersect(3, 4, 5), sets.superset(3, 4, 5))(3, 5) == [False, [3, 5], True]

def test_map():
    assert list(funcy.map(add(3))(range(5))) == list(map(add(3), range(5)))
    assert list(funcy.map(add(3), add(1))(range(5))) == list(map(add(4), range(5)))

def test_filter():
    is_odd = lambda x: x % 2
    assert list(funcy.filter(is_odd)(range(4))) == [1, 3]

def test_remove():
    is_even = lambda x: x % 2 == 0
    assert list(funcy.remove(is_even)(range(4))) == [1, 3]

