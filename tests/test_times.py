'Test times operators module'

import pytest
from funcypy.times import *

def test_epoch_iso_dt():
    assert epoch_to_iso(0) == '1970-01-01T00:00:00Z'
    assert iso_to_epoch(epoch_to_iso(0)[:-1]) == local_diff()
    assert epoch_to_iso(0, utc=False) == epoch_to_iso(0 - local_diff())[:-1]
    assert dt_from_iso(epoch_to_iso(0)).timestamp() == 0
    assert dt_from_iso(epoch_to_iso(0, utc=False)).timestamp() == 0
    assert iso_to_epoch(epoch_to_iso(0)) == 0
    assert iso_to_epoch(epoch_to_iso(0, utc=False)) == 0

def test_zulu_local():
    assert to_zulu(epoch_to_iso(0, utc=False)) == '1970-01-01T00:00:00Z' 
    assert to_zulu('1970-01-01T00:00:00Z') == '1970-01-01T00:00:00Z' 
    assert to_local('1970-01-01T00:00:00Z') == epoch_to_iso(0, utc=False)
    assert to_local(epoch_to_iso(0, utc=False)) == epoch_to_iso(0, utc=False)