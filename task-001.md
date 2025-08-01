# Task-001: A Module for Transducer-Like Operations

- maybe `mapinto`, or `partialmap`
- the equivalent of `map(rcomp(...))`
- I would prefer it to work at the iterator level
- but maybe I'm thinking of more like `mapintodict`
- what kind of things:
  - map(key/valfilter)
  - mapinto is map_partial:
    - where the map function itself is `@partial`'d
  - pcomp is partial'd rcomp:
    - but is it so bad to type partial(map)(...)

In clojure I made threading macros like `map->` with the purpose of putting the vale in the front like `pipe`, maybe what I want is more like `pipemap`

Maybe what I should consider instead is debugging
