# datafun-03-analytics

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> ETVL data pipelines in Python, applied to online gaming session data.

**Author:** Josiah Davis

**Docs:** <https://jgdavis24.github.io/datafun-03-analytics/>

## What this project does

Four pipelines, four file formats, one structure. Each follows the same
four stages: Extract, Transform, Verify, Load.

| Format | Input | Question |
|---|---|---|
| CSV | `player_sessions.csv` | How is net revenue per session distributed? |
| JSON | `astros.json` | How many astronauts are on each spacecraft? |
| XLSX | `Feedback.xlsx` | How often does feedback mention GitHub? |
| TXT | `romeo_and_juliet.txt` | How long is the document? |

The CSV pipeline is the one I made my own. The other three are the example
project's, left in place because they show the same structure working on
three more formats.

## The result

**Average session revenue is close to useless on its own.**

| Measure | Value |
|---|---|
| Sessions | 4,210 |
| Minimum | -$1,900.85 |
| Maximum | $3,735.54 |
| Mean | $18.48 |
| Standard deviation | $195.01 |

The standard deviation is about eleven times the mean. Sessions range from
a $1,900 loss to a $3,735 win around an average of eighteen dollars.

There is no such thing as a typical session. The mean is real arithmetic
on a wide, skewed distribution, and reporting it without the spread next
to it implies a stability the data does not have.

I wrote that prediction into `app.py` before running the pipeline, in the
`WHY_CSV_COLUMN` block. The point of stating it first is that it could
have been wrong.

Note the negative minimum. Revenue goes negative whenever a player wins.
Nothing in the pipeline assumes revenue is positive, which is why this
data ran through it without breaking.

## About the data

`player_sessions.csv` holds 4,210 synthetic sessions across 900 players,
with acquisition channel, game category, device, duration, bets placed,
and net revenue.

I spent four years in casino and iGaming analytics. None of that data can
go in a public repository, and anything committed to Git stays in the
history even after the file is deleted. Generating realistic structure is
how you demonstrate a pipeline in a regulated industry without creating a
problem you cannot undo.

The generator is in this repository at `scripts/make_session_data.py`. It
is seeded, so running it reproduces the same file:

```shell
uv run python scripts/make_session_data.py
```

Publishing numbers without publishing the code that produced them asks the
reader to take them on faith.

See the [data card](./docs/data-card.md) for field detail.

## Run it

```shell
git clone https://github.com/jgdavis24/datafun-03-analytics
cd datafun-03-analytics
code .
```

Then in a VS Code terminal, one command at a time:

```shell
uv sync
uv run python -m datafun.app
```

Output lands in `data/processed/`, one report per pipeline, and a
`project.log` appears in the project root.

## Project layout

- **data/raw/** - input files
- **data/processed/** - generated output, one report per pipeline
- **docs/** - project narrative and results
- **scripts/** - the synthetic data generator
- **src/datafun/**
  - `app.py` - declares the data choices and the reasoning, runs the pipelines
  - `utils_etvl.py` - reusable ETVL mechanics
  - `etvl_csv.py`, `etvl_json.py`, `etvl_xlsx.py`, `etvl_text.py` - format pipelines
- **tests/** - pytest suite

## What I changed from the example

**Technical modification.** Switched the CSV pipeline from `Ladder score`
to `Perceptions of corruption` in the world happiness data, and renamed
the output file to match. An output file whose name no longer describes
its contents is a small bug that becomes a real one later.

**Custom project.** Replaced the happiness data with synthetic player
session data, wrote the generator that produces it, and pointed the CSV
pipeline at net revenue per session.

**Not changed:** `utils_etvl.py`. The reusable extract, transform, verify,
and load functions moved from a national happiness survey to gaming
session data without a single edit. That is the lesson of the module:
`app.py` holds the decisions, `utils_etvl.py` holds the mechanics, and the
mechanics do not care what the data is about.

## Chores

```shell
uv run ruff format .
uv run ruff check . --fix
uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

## License

MIT. See [LICENSE](./LICENSE).
