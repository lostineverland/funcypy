# funcypy

Minimalist functional leaning library

# Development

This code is managed by [uv](https://docs.astral.sh/uv). When in TDD mode, I prefer to use [entr](https://github.com/eradman/entr) + [the_silver_searcher](https://github.com/ggreer/the_silver_searcher) to run the test suite:

```sh
funcypy=test ag -l '' (src|tests)/*py | entr -s "uv run python runtests.py -f vv"
```