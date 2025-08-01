# Task-004: Monitoring partial functions

```py
'looking at stacking decorators wrt tracking'

import functools
from typing import Callable, Any, Dict, Union
from funcypy import funcy
from funcypy.eager import cols

@track(frequency=1)
@partial
def add(a, b):
  return a + b

add3 = add(3)

add3 = functools.update_wrapper(functools.partial(add, 3), add)
isinstance(add3, functools.partial)


try:
  assert False, "assertion wins"
except Exception as e:
  print('nothing to see here')
```
