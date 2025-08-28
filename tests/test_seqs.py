'Test seqs operators module'

import pytest
from funcypy import seqs

@pytest.fixture()
def data():
    return iter(range(10))

is_odd = lambda x: x % 2

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
    assert list(seqs.concat(['some', 'thing'], ['some', 'more'])) == ['some', 'thing', 'some', 'more']
    assert list(seqs.concat(data, data)) == list(range(10))
    assert list(seqs.concat(range(3), range(3))) == 2 * list(range(3))
    # assert list(seqs.concat([range(3), range(3)])) == 2 * list(range(3))
    assert list(seqs.concat([], range(3), [], [3], [])) == list(range(4))

def test_iterator(data):
    assert list(seqs.iterator(range(10))) == list(range(10))
    ii = seqs.iterator(data)
    assert next(ii) == 0
    assert ii.send(-3) == None
    assert next(ii) == -3
    assert next(ii) == 1
    assert list(ii) == list(range(2, 10))

def test_select():
    assert seqs.select(is_odd, 1) == 1
    assert seqs.select(is_odd, 2) == None

def test_cond():
    is_even = lambda x: x % 2 == 0
    assert list(seqs.cond(
                is_even,
                lambda x: x**2,
            range(5))) == [i**2 if is_even(i) else i for i in range(5)] 
    assert list(seqs.cond(
                is_odd,
                lambda x: x**2,
            range(5))) == [i for i in range(5)] 
