'looking at stacking decorators wrt tracking'

import functools
from typing import Callable, Any, Dict, Union
from funcypy import funcy, monitor
from funcypy.seqs import concat
from funcypy.eager import cols, seqs

print('---'*20)

@monitor.track(frequency=1)
@funcy.partial
def add(a, b):
  return a + b

@funcy.partial
@monitor.track(frequency=1)
def mul(a, b):
  return a * b

add3 = add(3)
mul2 = mul(2)

# These behave as expected
# add3(5)
# mul2(5)
# add3('5')
# mul2('5')

# print(list(concat([2])))

funcy.pipe(10,
    mul(3),
    add(5),
    # seqs.concat(range(4)),
    # seqs.concat(),
    # {2, 35}.issuperset,
    funcy.has(35, 36),
    monitor={'frequency': 1}
    )

