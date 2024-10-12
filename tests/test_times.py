'Test times operators module'

import pytest
from funcypy.times import *

# these are dependent on my timezone, make it more general
def test_epoch_iso_dt():
    assert epoch_to_iso(0) == '1970-01-01T00:00:00Z'
    assert epoch_to_iso(0, utc=False) == '1969-12-31T19:00:00'
    assert dt_from_iso(epoch_to_iso(0)).timestamp() == 0
    assert dt_from_iso(epoch_to_iso(0, utc=False)).timestamp() == 0
    assert iso_to_epoch(epoch_to_iso(0)) == 0
    assert iso_to_epoch(epoch_to_iso(0, utc=False)) == 0
    assert iso_to_epoch(epoch_to_iso(0)[:-1]) == 18000

def test_zulu_local():
    assert to_zulu('1969-12-31T19:00:00') == '1970-01-01T00:00:00Z' 
    assert to_zulu('1970-01-01T00:00:00Z') == '1970-01-01T00:00:00Z' 
    assert to_local('1970-01-01T00:00:00Z') == '1969-12-31T19:00:00'
    assert to_local('1969-12-31T19:00:00') == '1969-12-31T19:00:00'