'Test seqs operators module'

import pytest
from funcypy.funcy import *

@partial
def add(x, y):
    print(f'{x} + {y}:', x + y)
    return x + y

@partial
def pow(y, x):
    print(f'{x} ** {y}:', x ** y)
    return x ** y

def test_rcomp_complement():
    assert rcomp(add(3), pow(2))(2) == 25
    assert complement(rcomp(add(3), pow(2)))(2) == False

def test_pipe():
    assert pipe(2, add(3), pow(2)) == 25

def test_contains():
    assert contains('some', 1, 'me')('some')
    assert has('some', 1, 'me')(1)
    assert not contains('some', 1, 'me')('other')
