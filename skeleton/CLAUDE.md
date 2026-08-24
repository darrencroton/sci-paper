# <paper short name>

A paper workspace. Sessions here work under the sci-paper skills.

**Workspace root:** `<workspace root>` --- every path below is relative to it.
`.` means this directory is the workspace.

## First action, every session

1. Read `paper/STATE.md` in full. It is capped at two pages so that it can be
   read whole, every time, without deciding whether to.
2. Read `<sci-paper>/skills/_shared/memory.md` and
   `<sci-paper>/skills/_shared/house-rules.md`.

Those two files are the authority on how to behave here. They are deliberately
not restated in this file, and nothing in this file overrides them. They apply
to ordinary conversation exactly as they apply to a `/paper-...` command --- the
commands are shortcuts, not an interface anyone has to learn.

## Directory map

Author-owned paths are the ones this paper actually uses --- edit the rows below
to match, and delete any that do not exist.

| Path | Owner | |
|---|---|---|
| `notes/` | author | free-form markdown; modified only on an explicit "capture that" |
| `figures/` | author | looked at, never regenerated |
| `code/` | author | read, never run |
| `paper/` | agent | the project's memory: `STATE.md`, `journal.md`, `outline.md`, `open-questions.md`, `lit/` |
| `manuscript/` | shared | the author edits this directly and constantly |
| `.build/` | build | gitignored |

`paper/`, `manuscript/` and `.build/` are always directly inside the workspace
root. The author's directories are wherever the author keeps them, which may be
outside it --- a path such as `../analysis/` is normal and correct.

Everything except `.build/` is committed. The diffs of `paper/` are the record
of how the paper was thought through.

## Venue

Not yet chosen --- `main.tex` uses a plain `article` class. Choosing one means
fetching the journal's current template and class file into `manuscript/` and
changing the preamble.

## Build

From the workspace root:

    (cd manuscript && latexmk -pdf -interaction=nonstopmode -outdir=../.build main.tex)

Keep `-interaction=nonstopmode`. Without it a LaTeX error waits at the
interactive `?` prompt and the build hangs instead of failing.

Draft mode is the default. Final mode is the `[final]` option on
\usepackage{scipaper} in `main.tex`; it fails the build while any `\gap`
remains.
