import datetime
from functools import partial

ISO_8601_YEARS = '%Y'
ISO_8601_MONTHS = '%Y-%m'
ISO_8601_WEEKS = '%G-W%V' # `%G` gives the year corresponding to the ISO week number (which may differ from the calendar year).
ISO_8601_DAYS = '%Y-%m-%d'
ISO_8601_HOURS = '%Y-%m-%dT%H'
ISO_8601_MINUTES = '%Y-%m-%dT%H:%M'
ISO_8601_SECONDS = '%Y-%m-%dT%H:%M:%S'
ISO_8601_MICROSECONDS = '%Y-%m-%dT%H:%M:%S.%f'

iso_formats = {
    'years': ISO_8601_YEARS,
    'months': ISO_8601_MONTHS,
    'weeks': ISO_8601_WEEKS,
    'days': ISO_8601_DAYS,
    'hours': ISO_8601_HOURS,
    'minutes': ISO_8601_MINUTES,
    'seconds': ISO_8601_SECONDS,
    'microseconds': ISO_8601_MICROSECONDS,
}

def format_granularity(iso_dt: str) -> str:
    "Determine the granularity of the iso_dt string based on it's length"
    len_to_format = {
        len(datetime.datetime.now().strftime(v)): v 
        for k, v in iso_formats.items()
    }
    return len_to_format.get(len(iso_dt), 'unknown_iso_dt')

def iso_ts(format, local=False):
    '''Where format is one of:
        years
        months
        weeks
        days
        hours
        minutes
        seconds
        microseconds
    '''
    if local:
        return datetime.datetime.now().strftime(iso_formats[format])
    else:
        return datetime.datetime.utcnow().strftime(iso_formats[format]) + 'Z'

now = partial(iso_ts, 'microseconds', local=True)
utc_now = partial(iso_ts, 'microseconds')
today = partial(iso_ts, 'days', local=True)
utc_today = partial(iso_ts, 'days')
week = partial(iso_ts, 'weeks', local=True)
utc_week = partial(iso_ts, 'weeks')
year = partial(iso_ts, 'years', local=True)
utc_year = partial(iso_ts, 'years')

def dt_from_iso(iso_dt):
    'always return UTC datetime'
    if iso_dt[-1] == 'Z':
        format = format_granularity(iso_dt[:-1])
        dt = datetime.datetime.strptime(iso_dt[:-1], format)
    else:
        format = format_granularity(iso_dt)
        dt = datetime.datetime.utcfromtimestamp(
            datetime.datetime.strptime(iso_dt, format).timestamp())
    return dt.replace(tzinfo=datetime.timezone.utc)

def epoch_to_iso(epoch, utc=True):
    if utc:
        return datetime.datetime.utcfromtimestamp(epoch).strftime(ISO_8601_SECONDS) + 'Z'
    else:
        return datetime.datetime.fromtimestamp(epoch).strftime(ISO_8601_SECONDS)

def iso_to_epoch(iso_dt):
    dt = dt_from_iso(iso_dt)
    return dt.timestamp()

def to_zulu(iso_dt):
    return epoch_to_iso(dt_from_iso(iso_dt).timestamp())

def to_local(iso_dt):
    return epoch_to_iso(dt_from_iso(iso_dt).timestamp(), utc=False)

def local_diff():
    return (datetime.datetime.utcfromtimestamp(0) - datetime.datetime.fromtimestamp(0)).total_seconds()