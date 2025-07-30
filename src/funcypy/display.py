'A collection of tools for displaying or pretty printing'

from . funcy import partial
from . import monitor

track = monitor.track(namespace=__name__)

@partial(count=2)
@track
def apply_format(val, fmt, num_fmt='{:,.7g}', str_fmt='{}'):
    if fmt:
        try:
            s = fmt.format(val)
        except:
            s = '_{}_'.format(val)
        return s
    elif isinstance(val, str):
        return str_fmt.format(val)
    else:
        return num_fmt.format(val)

@track
def table(rows, headers=None, rename={}, fmt={}, num_fmt='{:,.7g}', str_fmt='{}'):
    label = lambda k: rename.get(k, k)
    rev_rename = {v: k for k, v in rename.items()}
    rev_label = lambda l: rev_rename.get(l, l)
    if not headers:
        headers = set(k for row in rows for k in row)
    applyFormat = apply_format(num_fmt=num_fmt, str_fmt=str_fmt)
    heading = '|' + '|'.join(applyFormat(label(i), None) for i in headers) + '|'
    lineFmt = lambda line: '|' + '|'.join(applyFormat(line.get(rev_label(i)), fmt.get(i)) for i in headers) + '|'
    lines = list(lineFmt(row) for row in rows)
    return dict(heading=heading, lines=lines)

def dicts_to_table(rows, headers=None, rename={}, fmt={}, num_fmt='{:,.7g}', str_fmt='{}'):
    heading, lines = map(table(rows, headers, rename, fmt, num_fmt).get, ['heading', 'lines'])
    return '\n'.join([heading] + lines)
