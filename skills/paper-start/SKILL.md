---
name: paper-start
description: Ingest an astronomer's notes, figures, tables and analysis code, scaffold the paper workspace, and propose an argument spine plus the questions the material does not answer. Use at the beginning of a new paper, or when pointed at a directory of research material that has no manuscript yet.
---

# paper-start

Read everything the author has, look at every figure, and come back with three
things: **a proposed argument**, **the results as understood**, and **what could
not be worked out**. Then scaffold the workspace so the next session has
somewhere to stand.

This is a conversation, not a gate. It runs against thin, messy, incomplete
material — that is the normal case, not a failure. **A short outline and a long
question list is a good outcome.**

## Before anything

First, look whether there is anything to resume:

```sh
ls paper/STATE.md 2>/dev/null
```

**If it exists, this is not a new paper.** Read `paper/STATE.md` in full before
anything else, exactly as every other session does, then the shared files below,
then ask what the author wants re-ingested before touching a thing.

**If it does not, this is the one session in the project with no state to read**
— and the only one where the shared files come first.

Either way, read from the astro-paper installation (the directory holding this
skill — `../_shared/`; the paper repo's `CLAUDE.md` names the install path if
that does not resolve):

- `_shared/memory.md`
- `_shared/house-rules.md`

They are the authority and are not restated here.

## 1. Survey

```sh
for d in notes figures code tables; do
  if [ -d "$d" ]; then ls -R "$d"; else printf '%s: absent\n' "$d"; fi
done
[ -d data ] && printf 'data/: present, %s entries at top level\n' "$(ls data | wc -l | tr -d ' ')"
ls
```

Absence is information, not failure: `code/` is optional and a paper with no
analysis code is normal. The bare `ls` catches material the author left at the
top level or in a directory named something else entirely, which is common.

**`data/` is counted, never listed recursively.** A survey directory in
astronomy routinely holds millions of files, and `ls -R` on it would flood the
session before a single note has been read. If a specific data file or table
matters, the author will point at it.

Report what is there before reading it — how many notes, how many figures, is
there code, are there tables. The author often does not know either.

## 2. Read the notes and any tables

All of them, in full. They are author-owned: **read only.** Note as you go which
claims carry a number and where that number came from — those become the `% src:`
anchors later, so it is cheaper to capture them now.

Where a note says something you cannot map onto a result or a figure, that is a
question, not something to smooth over.

**Tables count as notes here and are read the same way.** They arrive as
standalone `.tex`, `.csv`, `.dat` or a fenced block inside a note, and they are
often where the real numbers live — a table row is a first-class `% src:` source
and a far better one than a value read off a plot. For each, record what the
columns are, their units and any $h$-scaling, and where the table came from.
A column whose header does not say its units is a question.

## 3. Look at every figure

Actually look at them. **PNG and PDF are opened and read directly** — a figure
is a single page and needs no conversion. EPS and PS cannot be read, so those,
and only those, get converted into `.build/` first:

```sh
mkdir -p .build
gs -q -dNOPAUSE -dBATCH -dEPSCrop -sDEVICE=png16m -r150 \
   -sOutputFile=.build/fig3.png figures/fig3.eps
```

`-dEPSCrop` is not decoration. Without it `gs` paints the figure onto a default
page and hands back a mostly blank US-Letter image with the plot small in one
corner — worse than an error, because it still looks like a figure. The line
assumes a single-page EPS, which is what a plotting library writes; for a
multi-page PostScript file put `%d` in the output name
(`-sOutputFile=.build/fig3-%d.png`), drop `-dEPSCrop`, and look at each page.

Rasterising a *built manuscript page* is a different job and does need
`pdftoppm -png -r 150 -singlefile .build/main.pdf .build/page1`, where
`-singlefile` matters: without it the output lands at `page1-1.png` and the read
fails.

For each figure record, in one or two lines — these are working notes now, and
the durable version of each one lands in the outline's **Figures** table at step
7, so nothing needs a file of its own:

- what is on each axis, **including the units and any $h$-scaling**
- what the different lines, points and colours are
- what it shows — the trend, and where the trend stops
- **whether the axis labels agree with what appears to be plotted, and whether
  both agree with the caption and the notes**

That last one is not a formality. In this author's own published work a
mislabelled axis — the wrong database column loaded, $V_{\rm max}$ plotted where
$V_{\rm vir}$ was labelled — produced a wrong conclusion in a paper with
thousands of citations, found only after publication by an outside reader. Any
mismatch goes straight into `open-questions.md`.

Expect the directory to be untidy: orphan assets, `.eps` and `.pdf` versions of
the same plot with different content, figures whose generator writes a different
extension than the manuscript includes. Say what you find; do not tidy it.

Note which figures are **EPS or PS only** — `pdflatex` cannot include those, so
they will need converting before any draft that uses them will build. Report it;
`/paper-draft` handles it when the figure is actually used.

## 4. Read the code, if there is any

Read, never run. Never modify. What matters here is: what does it actually
compute, what are the hard-coded constants and cuts, and what does it plot on
each axis. Data is often an inline literal with no column names at all — where
that is so, say the binding is unresolved rather than guessing.

## 5. Scaffold

Copy the skeleton from the astro-paper installation (`skeleton/`) into the paper
repo — `CLAUDE.md`, `.gitignore`, `paper/`, `manuscript/`:

```sh
for f in CLAUDE.md .gitignore manuscript/main.tex manuscript/astropaper.sty; do
  [ -e "$f" ] && printf 'pre-existing, leave alone: %s\n' "$f"
done
cp -Rn "<astro-paper>/skeleton/." .
mkdir -p notes figures code manuscript/sections
```

Every part of that earns its place:

- **The first loop** names what is already there. `cp -Rn` preserves existing
  files but does not report what it skipped, and the placeholder step below needs
  to know the difference.
- **`-n`** is what makes "never overwrite" true rather than merely intended. A
  plain `cp -R` silently replaces a `CLAUDE.md` or a `main.tex` the author has
  spent a week editing.
- **The quotes** matter because an installation path may contain a space.
- **`manuscript/sections/`** must be created explicitly. Git does not track
  empty directories, so it cannot ship in the skeleton, and `/paper-draft`
  writes its first section straight into it — without this, that write fails on
  a brand new workspace. `mkdir -p` leaves the other three alone if they exist.

Then substitute the placeholders — the paper's short name, the author list, the
install path — **only in the files the copy actually created.** A `CLAUDE.md` or
a `main.tex` that was already there belongs to the author, has no placeholders
left in it, and is not to be rewritten in the name of scaffolding. Say which
files you left alone.

## 6. The venue

Ask which journal, and **accept "not decided yet"** — early on it usually is
not, and refusing to start until the author picks one would be exactly the wrong
gate. The skeleton uses a plain `article` class and switching later is a
preamble change plus a re-fetch; the prose does not care.

If a venue *is* named, fetch its current template. Four things about how:

- **From the journal's own author or submission pages.** Not a mirror, not a
  copy bundled with somebody else's paper, and never written from memory. Find
  those pages for this journal rather than assuming a URL; they move.
- **Take the whole bundle, not just the `.cls`.** A journal class normally needs
  its `.bst` and its style files alongside it to compile at all.
- **Build once before moving on.** A template that does not compile is far
  better discovered now than at submission.
- **Record the URL and the date** in the journal entry. "Which version of this
  class is it?" gets asked months later, and classes drift continuously — a
  stale one is what gets a submission bounced before review.

If it cannot be fetched, say so, leave the plain `article` scaffold in place,
and carry it as an open question. Do not hand-write a class file.

## 7. Propose the argument

Write `paper/outline.md`. It is the **sole authority for the argument** and
everything downstream reads it.

```markdown
# Outline

**Claim:** <one sentence — what this paper establishes. If the material does not
support a single sentence yet, say so here and make that the first open question.>

## Spine
1. <step in the argument> — rests on: <fig 3 / notes/methods.md / code/sam/>
2. ...

Each step must rest on something that exists. A step resting on nothing is the
paper's real open question.

## Sections
| # | Heading | Role | Carries |
|---|---|---|---|
| 1 | Introduction | framing | — |
| 2 | The galaxy formation model | methods | code/sam/ |
| 3 | Results | results | Fig 3–5 |
| 4 | Physical interpretation | discussion | — |
| 5 | Conclusions | framing | — |

Headings are whatever this paper actually uses; the **role** column is what
`/paper-draft` keys on, and it holds only the bare words `methods`, `results`,
`discussion`, `framing` — joined by ` + ` where a section carries more than one,
so a combined "Results and Discussion" is one row reading `results + discussion`.
Those words are filenames in `_shared/sections/`, which is why nothing else goes
in the cell. A paper with no results section is allowed.

## Figures
| File | Shows | Lands in |
|---|---|---|
```

Propose it, then **discuss it**. Do not present it as decided.

## 8. Say what you could not work out

Write `paper/open-questions.md` in the format `_shared/memory.md` gives. Be
generous — this is the most useful output of the whole skill. Typical entries:

- a note claims a number no figure or code produces
- two notes disagree
- a figure exists that nothing explains
- an axis label that does not match the plot or the caption
- the cosmology or $h$-convention is never stated
- the sample cut is stated with no reason
- a result that is clearly the point of the paper, with nothing behind it yet

**Never invent a result to fill a hole.** If the notes do not say what the paper
found, the paper does not yet know, and that is the finding.

## 9. Report back

In conversation, not as a file dump:

- what is here (n notes, n figures, code or not)
- the proposed claim, in one sentence
- the results as understood, briefly
- the questions, ordered by how much they block
- what to do next — usually `/paper-draft` on the role with the most material

## 10. Close the session

Write `paper/STATE.md` and append the `paper/journal.md` entry, per
`_shared/memory.md`. `STATE.md`'s *Next* names the next section to draft.
