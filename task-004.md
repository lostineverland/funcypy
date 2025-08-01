# Task-004: Monitoring partial functions

The partial function is getting in the way of monitor.track, the same will apply to generator functions, but I will deal with that later.

I'm going to create a canonical example so that I can better find a solution.

# Refs
- [`issue.py`][./issue-004/issue.py]


# Methodology

```sh
funcyp=issue ag -l '' *py ../../src/*py | entr -s "uv run python issue.py"
```