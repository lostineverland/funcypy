'Test collection operators module'

import pytest
from funcypy.eager import cols

@pytest.fixture()
def data():
    return dict(some=1, me=2)

def test_keymap(data):
    assert cols.keymap(str.upper, data) == dict(SOME=1, ME=2)
    assert cols.keymap(str.upper)(data) == dict(SOME=1, ME=2)

def test_valmap(data):
    add_1 = lambda x: x + 1
    assert cols.valmap(add_1, data) == dict(some=2, me=3)
    assert cols.valmap(add_1)(data) == dict(some=2, me=3)

def test_itemmap(data):
    swap = lambda x, y: (y, x)
    assert cols.itemmap(swap, data) == dict(((1, 'some'), (2, 'me')))
    assert cols.itemmap(swap)(data) == dict(((1, 'some'), (2, 'me')))

def test_keyfilter(data):
    is_some = lambda x: x == 'some'
    assert cols.keyfilter(is_some, data) == dict(some=1)
    assert cols.keyfilter(is_some)(data) == dict(some=1)

def test_valfilter(data):
    is_odd = lambda x: x % 2
    assert cols.valfilter(is_odd, data) == dict(some=1)
    assert cols.valfilter(is_odd)(data) == dict(some=1)

def test_removekey(data):
    is_me = lambda x: x == 'me'
    assert cols.removekey(is_me, data) == dict(some=1)
    assert cols.removekey(is_me)(data) == dict(some=1)

def test_removeval(data):
    is_even = lambda x: x % 2 == 0
    assert cols.removeval(is_even, data) == dict(some=1)
    assert cols.removeval(is_even)(data) == dict(some=1)

def test_removevalnone(data):
    d = {**data, 'on': 3, 'what': None}
    assert cols.removevalnone(d) == dict(some=1, me=2, on=3)

def test_field_filter(data):
    sample = dict(some=1, me=2, on=3, what=4)
    assert list(map(cols.field_filter(['some', 'me', 'for']), 3 * [sample])) == 3 * [data]

def test_flatten():
    data = {"some": {"nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "other": 3}}
    assert cols.flatten(data) == {"some.nested.value1": 1, "some.nested.value2": [{"more":{"nesting": 3}}, {"value4": 4}], "some.other": 3}
    assert cols.flatten(data, depth=1) == {"some.nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "some.other": 3}
    assert cols.flatten(data, follow_list=True) == {"some.nested.value1": 1, "some.nested.value2.0.more.nesting": 3, "some.nested.value2.1.value4": 4, "some.other": 3}

def test_nestten():
    data = {"some.nested.value1": 1, "some.nested.value2.0.more.nesting": 3, "some.nested.value2.1.value4": 4, "some.other": 3}
    resp = {"some": {"nested": {"value1": 1, "value2": [{"more":{"nesting": 3}}, {"value4": 4}]}, "other": 3}}
    assert dict(cols.nestten(cols.flatten(resp, follow_list=True))) == resp
    assert cols.nestten(data) == resp
