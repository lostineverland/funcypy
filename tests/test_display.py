'Test display module'

import pytest
from funcypy import display


@pytest.fixture()
def data():
    return [{'x': x, 'y0': 3*x, 'y1': x*x} for x in range(20)]

def test_table(data):
    # assert map(dict.keys, data) == set(list(k for k in row.keys()) for row in data)
    assert sorted(display.table(data)['heading']) == sorted('|x|y0|y1|')
    assert display.table(data, headers=['x', 'y0', 'y1'], str_fmt=' {} ', num_fmt=' {} ')['lines'][0] == '| 0 | 0 | 0 |'
    assert display.dicts_to_table(data[10:11], headers=['x', 'y0', 'y1'], rename={'x': ' t '}, str_fmt=' {} ', num_fmt=' {} ') == '| t |y0|y1|\n| 10 | 30 | 100 |'
    assert display.table(data, headers=['t', 'y0', 'y1'], fmt={'y0': '{:06.2f}'}, rename={'x': 't'}, str_fmt=' {} ', num_fmt=' {} ')['lines'][10] == '| 10 |030.00| 100 |'
    assert display.dicts_to_table([dict(some=1, me=1), dict(some=2, me=2, on=[3])], headers=['some', 'me', 'on']) == '|some|me|on|\n|1|1|-|\n|2|2|[3]|'
