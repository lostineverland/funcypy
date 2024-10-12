import datetime

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

now = lambda: datetime.datetime.now().strftime(ISO_8601_MICROSECONDS)
utc_now = lambda: datetime.datetime.utcnow().strftime(ISO_8601_MICROSECONDS) + 'Z'
today = lambda: datetime.datetime.now().strftime(ISO_8601_DAYS)
utc_today = lambda: datetime.datetime.utcnow().strftime(ISO_8601_DAYS) + 'Z'
week = lambda: datetime.datetime.now().strftime(ISO_8601_WEEKS)
utc_week = lambda: datetime.datetime.utcnow().strftime(ISO_8601_WEEKS) + 'Z'

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
