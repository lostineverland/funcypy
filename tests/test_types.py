'Test types module'

import pytest
from funcypy import types


@pytest.fixture()
def data():
    return iter(range(10))

def test_is_lazy(data):
    def loop():
        for i in range(10):
            yield i
    assert types.is_lazy(data)
    assert types.is_lazy(loop())
    assert types.is_lazy(i for i in data)
    assert not types.is_lazy(range(10))
    assert not types.is_lazy([i for i in data])

def test_is_iterable(data):
    assert types.is_iterable(data)
    assert types.is_iterable(range(5))
    assert types.is_iterable([1, 2, 3])
    assert types.is_iterable((1, 2, 3))
    assert types.is_iterable('abc')
    assert not types.is_iterable(123)

