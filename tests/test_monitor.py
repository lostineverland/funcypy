'Test monitor module'

import pytest
import json, datetime
from funcypy import monitor
from funcypy.funcy import pipe, rcomp, partial
from funcypy import times

@partial
def add(x, y):
    # print(f'{x} + {y}:', x + y)
    return x + y

@partial
def pow(y, x):
    # print(f'{x} ** {y}:', x ** y)
    return x ** y

def test_track_rcomp(capsys):
    rcomp(add(3), monitor=dict(namespace='me'))(2)
    std = capsys.readouterr()
    assert json.loads(std.out)['namespace'] == 'me'
    rcomp(add(3), pow(2), monitor=dict(frequency=lambda x: x == 3))(2)
    std = capsys.readouterr()
    assert std.out == ''
    rcomp(add(3), pow(2), monitor=dict(frequency=lambda x: x == 25, namespace='me'))(2)
    std = capsys.readouterr()
    assert json.loads(std.out)['namespace'] == 'me'
    try:
        rcomp(add(3))('a')
    except:
        pass
    std = capsys.readouterr()
    assert json.loads(std.out)['args'] == ["a"]

def test_track_pipe(capsys):
    pipe(2, add(3), monitor=dict(namespace='some'))
    std = capsys.readouterr()
    assert json.loads(std.out)['namespace'] == 'some'
    pipe(2, add(3), pow(2), monitor=dict(frequency=lambda x: x == 3))
    std = capsys.readouterr()
    assert std.out == ''
    pipe(2, add(3), pow(2), monitor=dict(frequency=lambda x: x == 25, namespace='some'))
    std = capsys.readouterr()
    assert json.loads(std.out)['namespace'] == 'some'

def test_json_serializer():
    assert json.loads(json.dumps(
        Exception('some error', 'some arg'),
        default=monitor.json_serializer
    )) == {
        "type": "Exception",
        "message": "('some error', 'some arg')",
        "args":
        [
            "some error",
            "some arg"
        ],
        "traceback": "Exception: ('some error', 'some arg')\n"}
    assert json.dumps(
            set([1, 2]),
            default=monitor.json_serializer,
        ) == '"{}"'.format(str({1, 2}))
    dt = datetime.datetime.now()
    assert json.dumps(
            dt,
            default=monitor.json_serializer,
        ) == '"{}"'.format(times.epoch_to_iso(dt.timestamp()))
