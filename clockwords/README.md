# clockwords (Python)

Word-clock phrase generator. Produces human-readable descriptions of every
minute of the day ("quarter past three", "twenty to midnight", …).

For the original TypeScript implementation see `../tsclockwords/`.

## Setup

```bash
# from the clockwords/ directory
uv sync --extra dev            # install package + dev tools (pytest, ruff, mypy)
uv sync --extra dev --extra ml # also pull in numpy / scipy / optuna
```

`uv` creates and manages `.venv` automatically — no manual activation needed.

## Tasks

```bash
uv run poe test       # run all tests
uv run poe lint       # ruff check + mypy
uv run poe fmt        # auto-format with ruff
uv run poe dump-menu  # dump TimeMenu to tmp/TimeMenu.kv.json
```

## Tests

```bash
uv run pytest                  # run all tests
uv run pytest -v               # verbose output
uv run pytest --cov=clockwords # with coverage report
```

## Linting / type-checking

```bash
uv run ruff check src tests    # lint
uv run ruff format src tests   # auto-format
uv run mypy                    # type-check src/
```

## Scripts

```bash
# Dump the full TimeMenu (all 1440 minutes × all phrase variants)
# to tmp/TimeMenu.kv.json in line-oriented KV-JSON format
uv run scripts/dump_time_menu.py
```

The output file is valid JSON as a whole and valid TSV line-by-line:

```
{	"00:00"	:	[{"hour":0,"min":0,"timewords":"twelve","words":"twelve"}, …]
,	"00:01"	:	[…]
…
}
```

## Package layout

```
src/clockwords/
  timewords.py   — vocabulary tables (HOUR_WORDS, MINUTE_PAST_WORDS, …) and helpers
  phrases.py     — TimePhrase dataclass
  templates.py   — TimeTemplate subclasses (ClockfaceHour, HalfPastHour, …)
  menu.py        — TIME_MENU dict and phrases_for() lookup
  kv_json.py     — dump_kv_json() helper for the line-oriented format
tests/
  test_clockwords.py
scripts/
  dump_time_menu.py
```
