'looking at stacking decorators wrt tracking'

import functools
from typing import Callable, Any, Dict, Union
from funcypy import funcy, monitor
from funcypy.eager import cols

print('---'*20)

@monitor.track(frequency=1)
@funcy.partial
def add(a, b):
  return a + b

@funcy.partial
@monitor.track(frequency=1)
def mul(a, b):
  return a + b

add3 = add(3)
mul2 = mul(2)

add3(5)
mul2(5)

# both of these work as expected
add3('5')
mul2('5')