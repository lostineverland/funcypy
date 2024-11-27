'Test monitor module'

import pytest
import json
from funcypy.funcy import pipe, rcomp, partial

@partial
def add(x, y):
    # print(f'{x} + {y}:', x + y)
    return x + y

@partial
def pow(y, x):
    # print(f'{x} ** {y}:', x ** y)
    return x ** y

def test_track_rcomp(capsys):
    assert rcomp(add(3), debug=dict(namespace='me'))(2)
    std = capsys.readouterr()
    assert json.loads(std.out)['namespace'] == 'me'

def test_track_pipe(capsys):
    pipe(2, add(3), debug=dict(namespace='some'))
    std = capsys.readouterr()
    assert json.loads(std.out)['namespace'] == 'some'

