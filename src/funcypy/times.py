import datetime

ISO_8601_YEARS = '%Y'
ISO_8601_MONTHS = '%Y-%m'
ISO_8601_WEEKS = '%Y-%V'
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

now = lambda: datetime.datetime.now().strftime(ISO_8601_MICROSECONDS)
utc_now = lambda: datetime.datetime.utcnow().strftime(ISO_8601_MICROSECONDS) + 'Z'
today = lambda: datetime.datetime.now().strftime(ISO_8601_DAYS)
utc_today = lambda: datetime.datetime.utcnow().strftime(ISO_8601_DAYS)


def dt_from_iso(iso_dt, format='minutes'):
    return datetime.datetime.strptime(iso_dt, iso_formats[format])

def epoch_to_iso(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime(ISO_8601_SECONDS)
