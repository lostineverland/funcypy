'Test times operators module'

import pytest
from funcypy.times import *

def test_epoch_iso_dt():
    assert epoch_to_iso(0) == '1970-01-01T00:00:00Z'
    assert dt_from_iso(epoch_to_iso(0)).timestamp() == 0
    assert dt_from_iso(epoch_to_iso(0, utc=False)).timestamp() == 0
    assert iso_to_epoch(epoch_to_iso(0)) == 0
    assert iso_to_epoch(epoch_to_iso(0, utc=False)) == 0
    iso_dt_micro = now()[:-2] + '00'
    iso_dt_deci = iso_dt_micro[:-2]
    assert dt_from_iso(iso_dt_deci) == dt_from_iso(iso_dt_micro)
    iso_dt_micro = now()[:-3] + '000'
    iso_dt_milli = iso_dt_micro[:-3]
    assert dt_from_iso(iso_dt_milli) == dt_from_iso(iso_dt_micro)
    iso_dt_micro = now()[:-3] + '000Z'
    iso_dt_milli = iso_dt_micro[:-3] + 'Z'
    assert dt_from_iso(iso_dt_milli) == dt_from_iso(iso_dt_micro)
    iso_dt_micro = now()
    iso_dt_nano = iso_dt_micro + '000'
    assert dt_from_iso(iso_dt_nano) == dt_from_iso(iso_dt_micro)

def test_zulu_local():
    assert to_zulu(epoch_to_iso(0, utc=False)) == '1970-01-01T00:00:00Z' 
    assert to_zulu('1970-01-01T00:00:00Z') == '1970-01-01T00:00:00Z' 
    assert to_local('1970-01-01T00:00:00Z') == epoch_to_iso(0, utc=False)
    assert to_local(epoch_to_iso(0, utc=False)) == epoch_to_iso(0, utc=False)
