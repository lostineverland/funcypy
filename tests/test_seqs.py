'Test seqs operators module'

import pytest
from funcypy import seqs
from funcypy.eager import seqs as eseqs

@pytest.fixture()
def data():
    return iter(range(10))

def test_is_lazy(data):
    def loop():
        for i in range(10):
            yield i
    assert seqs.is_lazy(data)
    assert seqs.is_lazy(loop())
    assert seqs.is_lazy(i for i in data)
    assert not seqs.is_lazy(range(10))
    assert not seqs.is_lazy([i for i in data])

def test_is_iterable(data):
    assert seqs.is_iterable(data)
    assert seqs.is_iterable(range(5))
    assert seqs.is_iterable([1, 2, 3])
    assert seqs.is_iterable((1, 2, 3))
    assert seqs.is_iterable('abc')
    assert not seqs.is_iterable(123)

def test_take(data):
    assert list(seqs.take(2)(data)) == [0, 1]

def test_limit_seq(data):
    assert list(seqs.limit_seq(4, data)) == list(range(4))

def test_loop():
    assert list(seqs.take(12, seqs.loop(4))) == 12 * [4]
    assert list(seqs.take(12, seqs.loop([4]))) == 12 * [4]
    assert list(seqs.take(7, seqs.loop([4, 3]))) == (6 * [4, 3])[:7]


def test_nth(data):
    assert seqs.nth(5)(data) == 4
    

def test_last(data):
    assert seqs.last(data) == 9
    assert seqs.last([]) == None

def test_concat(data):
    assert list(seqs.concat(data, data)) == list(range(10))
    assert list(seqs.concat(iter(range(3)), iter(range(3)))) == 2 * list(range(3))
    assert list(seqs.concat([], iter(range(3)), [], [3], [])) == list(range(4))

def test_iterator(data):
    assert list(seqs.iterator(range(10))) == list(range(10))
    ii = seqs.iterator(data)
    assert next(ii) == 0
    assert ii.send(-3) == None
    assert next(ii) == -3
    assert next(ii) == 1
    assert list(ii) == list(range(2, 10))

def test_concat():
    assert eseqs.concat()(3) == [3]
    assert eseqs.concat(3, 4) == [3, 4]
    assert eseqs.concat([3, 4], [5, 6]) == [3, 4, 5, 6]
    assert eseqs.concat(3, 4, [5, 6]) == [3, 4, 5, 6]
