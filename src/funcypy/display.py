'A collection of tools for displaying or pretty printing'

from . funcy import partial


@partial(count=2)
def apply_format(val, fmt, num_fmt='{:,.7g}', str_fmt='{}'):
    if fmt:
        return fmt.format(val)
    elif isinstance(val, str):
        return str_fmt.format(val)
    else:
        return num_fmt.format(val)

def table(rows, headers=None, rename={}, fmt={}, num_fmt='{:,.7g}', str_fmt='{}'):
    label = lambda k: rename.get(k, k)
    if not headers:
        headers = set(k for row in rows for k in row)
    applyFormat = apply_format(num_fmt=num_fmt, str_fmt=str_fmt)
    heading = '|' + '|'.join(applyFormat(label(i), None) for i in headers) + '|'
    lineFmt = lambda line: '|' + '|'.join(applyFormat(v, fmt.get(k)) for k, v in line.items()) + '|'
    lines = list(lineFmt(row) for row in rows)
    return dict(heading=heading, lines=lines)

def dicts_to_table(rows, headers=None, rename={}, fmt={}, num_fmt='{:,.7g}', str_fmt='{}'):
    heading, lines = map(table(rows, headers, rename, fmt, num_fmt).get, ['heading', 'lines'])
    return '\n'.join([heading] + lines)
