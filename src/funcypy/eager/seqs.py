'Operating on sequences'

import functools
from typing import List, Iterable
from .. funcy import partial
from .. import seqs


@partial
def concat(*seq: Iterable) -> List:
    return list(seqs.concat(*seq))

