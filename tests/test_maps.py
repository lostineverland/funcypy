'Test collection operators module'

import pytest
from funcypy import maps

@pytest.fixture()
def data():
    return dict(some=1, me=2)

odd = lambda i: i % 2

# def test_filter():
#     assert maps.filter(odd, range(5)) == [1, 3]

# def test_remove():
#     assert maps.remove(odd, range(5)) == [0, 2, 4]

def test_keymap(data):
    assert maps.keymap(str.upper, data) == dict(SOME=1, ME=2)
    assert maps.keymap(str.upper)(data) == dict(SOME=1, ME=2)

def test_valmap(data):
    add_1 = lambda x: x + 1
    assert maps.valmap(add_1, data) == dict(some=2, me=3)
    assert maps.valmap(add_1)(data) == dict(some=2, me=3)

def test_itemmap(data):
    swap = lambda x, y: (y, x)
    assert maps.itemmap(swap, data) == dict(((1, 'some'), (2, 'me')))
    assert maps.itemmap(swap)(data) == dict(((1, 'some'), (2, 'me')))

def test_keyfilter(data):
    is_some = lambda x: x == 'some'
    assert maps.keyfilter('some', data) == dict(some=1)
    assert maps.keyfilter('som', data) == dict()
    assert maps.keyfilter(is_some, data) == dict(some=1)
    assert maps.keyfilter(is_some)(data) == dict(some=1)
    sample = dict(some=1, me=2, on=3, what=4)
    assert list(map(maps.keyfilter(['some', 'me', 'for']), 3 * [sample])) == 3 * [data]

def test_valfilter(data):
    is_odd = lambda x: x % 2
    assert maps.valfilter(is_odd, data) == dict(some=1)
    assert maps.valfilter(is_odd)(data) == dict(some=1)

def test_removekey(data):
    is_me = lambda x: x == 'me'
    assert maps.removekey('me', data) == dict(some=1)
    assert maps.removekey(is_me, data) == dict(some=1)
    assert maps.removekey(is_me)(data) == dict(some=1)
    sample = dict(some=1, me=2, on=3, what=4)
    assert list(map(maps.removekey(['on', 'what']), 3 * [sample])) == 3 * [data]

def test_removeval(data):
    is_even = lambda x: x % 2 == 0
    assert maps.removeval(is_even, data) == dict(some=1)
    assert maps.removeval(is_even)(data) == dict(some=1)

def test_removevalnone(data):
    d = {**data, 'on': 3, 'what': None}
    assert maps.removevalnone(d) == dict(some=1, me=2, on=3)

def test_field_filter(data):
    sample = dict(some=1, me=2, on=3, what=4)
    assert list(map(maps.field_filter(['some', 'me', 'for']), 3 * [sample])) == 3 * [data]

def test_flatten():
    data = {"some": {"nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "other": 3}}
    assert maps.flatten(data) == {"some.nested.value1": 1, "some.nested.value2": [{"more":{"nesting": 3}}, {"value4": 4}], "some.other": 3}
    assert maps.flatten(data, depth=1) == {"some.nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "some.other": 3}
    assert maps.flatten(data, follow_list=True) == {"some.nested.value1": 1, "some.nested.value2.0.more.nesting": 3, "some.nested.value2.1.value4": 4, "some.other": 3}

def test_nestten():
    data = {"some.nested.value1": 1, "some.nested.value2.0.more.nesting": 3, "some.nested.value2.1.value4": 4, "some.other": 3}
    resp = {"some": {"nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "other": 3}}
    assert dict(maps.nestten(maps.flatten(resp, follow_list=True))) == resp
    assert maps.nestten(data) == resp

def test_pluck():
    points = [{'x': i, 'y0': i**2 , 'y1': i**3} for i in range(3)]
    assert maps.pluck('y1')(points[0]) == [i**3 for i in range(3)][0]
    assert maps.pluck('y1', points) == [i**3 for i in range(3)]
    assert maps.pluck(['x', 'y0'])(points) == [[i, i**2] for i in range(3)]
    assert maps.pluck(['x', 'y0'])(points[2]) == [[i, i**2] for i in range(3)][2]

def test_reduce():
    points = [{'x': i, 'y0': i**2 , 'y1': i**3} for i in range(3)]
    avg = lambda mem, y0, y1, y0sum, y1sum, count: dict(y0sum=(y0+y0sum*count)/(count+1), y1sum=(y1+y1sum*count)/(count+1), count=count+1)
    init = dict(y0sum=0, y1sum=0, count=0)
    assert maps.reduce(['y0', 'y1', 'y0sum', 'y1sum', 'count'], avg, points, init) == dict(y0sum=sum([i**2 for i in range(3)])/3, y1sum=sum([i**3 for i in range(3)])/3, count=3)
    assert maps.reduce(['y0', 'y1', 'y0sum', 'y1sum', 'count'], avg, init=init)(points) == dict(y0sum=sum([i**2 for i in range(3)])/3, y1sum=sum([i**3 for i in range(3)])/3, count=3)

