# learn_jq

A terminal course for learning [jq](https://jqlang.github.io/jq/), the JSON processor. Five stages, twenty-four lessons, from `.` to `tostream`.

## Requirements

- Python 3.10+
- `jq` 1.7+ on `PATH`

No third-party Python packages are required to run the course. `pytest` is only needed to run the test suite.

## Run

From the repo root:

```sh
python3 -m learn_jq
```

### Keys

| Action | Key |
|---|---|
| Run the filter you typed | `Enter` |
| Next lesson (once current passes) | `Tab` (or `Enter` on an empty filter) |
| Previous lesson | `Shift+Tab` or `F3` |
| Toggle hint | `F1` |
| Reveal expected output | `F2` |
| Reset the filter buffer | `Ctrl+U` |
| Scroll output up / down | `PgUp` / `PgDn` |
| Quit | `Esc` or `Ctrl+C` |

### How a lesson works

Each lesson shows a JSON input, a short explanation, and (once you ask for it) the expected output. Type a jq filter on the `FILTER>` line and press Enter. The course runs your filter with `jq -c`, parses each output value, and compares it to the expected stream — key order in objects is ignored, so multiple equivalent filters all pass.

### Stages

1. **Basics** — identity, field access, array indexing, bracket form
2. **Pipes & Slices** — pipe, slicing, `.[]`, comma
3. **Transformation** — object/array construction, `map`, `select`, `length`/`keys`
4. **Advanced** — `group_by`, `reduce`, `as`, `if/then/else`, `|=`
5. **Expert** — custom functions, regex `capture`, `recurse`, `del`/paths, `tostream`

## Test

```sh
python3 -m pip install pytest
python3 -m pytest tests/ -q
```

The lesson self-test runs every lesson's reference filter against its input and asserts the output matches the expected output, so any lesson typo fails the suite.

## Layout

```
learn_jq/
  __main__.py        entry point
  app.py             curses loop + key dispatch
  ui.py              pane layout + status line
  editor.py          filter input buffer
  validator.py       run jq, normalize, deep-compare
  progress.py        Progress protocol + InMemoryProgress
  models.py          Lesson, Stage
  lessons/           one file per stage
tests/               pytest suite
```

## Progress

By default, lesson progress is persisted to `$XDG_DATA_HOME/learn_jq/progress.json` (falls back to `~/.local/share/learn_jq/progress.json`). On launch the course resumes at the first unsolved lesson.

```sh
python3 -m learn_jq                              # default: persist to disk
python3 -m learn_jq --in-memory                  # do not save anything
python3 -m learn_jq --progress-file ./my.json    # custom location
python3 -m learn_jq --reset                      # wipe saved progress and start over
```
