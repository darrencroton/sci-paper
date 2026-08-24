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

First, look whether there is anything to resume. The workspace may be this
directory or a subdirectory of it, so look both places:

```sh
ls paper/STATE.md */paper/STATE.md 2>/dev/null
grep -l 'sci-paper: begin' CLAUDE.md 2>/dev/null
```

**If either finds something, this is not a new paper.** The workspace root is the
directory holding `paper/`, and `CLAUDE.md` names it. Read `paper/STATE.md` in
full before anything else, exactly as every other session does, then the shared
files below, then ask what the author wants re-ingested before touching a thing.

**If it does not, this is the one session in the project with no state to read**
— and the only one where the shared files come first.

Either way, read from the sci-paper installation (the directory holding this
skill — `../_shared/`):

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

### 1a. Settle the workspace root before anything writes a path

Do this now, not at §5. Everything after this point — the figure conversions in
§3, `.build/`, every path in every later session — is relative to the workspace
root, and a `.build/` created before the root is known is litter left in someone
else's project directory.

`_shared/house-rules.md` has the rule. Propose from what the survey just showed
and get a yes:

- **A named subdirectory, `paper-<short name>`** — the default when the working
  directory is already a project: it has its own `.git`, or a `src/`, or a
  `CLAUDE.md` about something else, or material with nothing to do with this
  paper. The paper then sits inside the project without taking it over.
- **`.`** — when the working directory *is* the paper: empty, or holding only
  this paper's material, or made for it.

Say which you propose and why in one sentence, ask for the short name if a
subdirectory, then create it. It is written `<ws>` from here on.

```sh
mkdir -p "<ws>"
```

Nothing the author owns moves into it, then or later.

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

**This is the step that makes the working directory work.** Everything the
skills need afterwards — the workspace root, the memory protocol, the install
path, the build command — is wired in here or is not wired in at all.

The workspace root (`<ws>`) was settled in §1a. Resolve **the installation
root** now, per *Locating the installation* in `_shared/house-rules.md`; it is
written `<sci-paper>` below and is never guessed.

### 5a. Copy the skeleton into the workspace root

```sh
mkdir -p "<ws>"
for f in "<ws>/manuscript/main.tex" "<ws>/manuscript/scipaper.sty"; do
  [ -e "$f" ] && printf 'pre-existing: %s\n' "$f"
done
cp -Rn "<sci-paper>/skeleton/paper" "<sci-paper>/skeleton/manuscript" "<ws>/"
mkdir -p "<ws>/manuscript/sections"
```

Every part of that earns its place:

- **`paper/` and `manuscript/` only.** The skeleton's `CLAUDE.md` and
  `.gitignore` belong at the *working-directory* root, not in the workspace, and
  §5b and §5c place them. Copying `skeleton/.` wholesale puts a `CLAUDE.md`
  where nothing loads it automatically.
- **The loop** names what is already there. `cp -Rn` preserves existing files
  but does not report what it skipped, and §5d needs to know the difference.
- **`-n`** is what makes "never overwrite" true rather than merely intended. A
  plain `cp -R` silently replaces a `main.tex` the author has spent a week
  editing.
- **The quotes** matter because either path may contain a space.
- **`manuscript/sections/`** must be created explicitly. Git does not track
  empty directories, so it cannot ship in the skeleton, and `/paper-draft`
  writes its first section straight into it — without this, that write fails on
  a brand new workspace.

**The author's three directories are found, not placed** —
`_shared/house-rules.md` is the authority. Use `notes/`, `figures/` and `code/`
wherever the survey found them, under whatever they are already called. Create
them inside `<ws>` **only** for material that exists nowhere:

```sh
# only for those the survey found nothing for, anywhere
mkdir -p "<ws>/notes" "<ws>/figures"
```

Never move or copy the author's existing material to make the layout match a
diagram.

### 5b. Wire `CLAUDE.md` at the working-directory root

**This is the load-bearing file.** It is the one a new session reads
automatically, so it is what names the workspace root and points at
`paper/STATE.md`. Skip it and the workspace looks scaffolded but the memory
protocol never engages.

If there is **no** `CLAUDE.md`, copy the skeleton's and fill it in:

```sh
cp -n "<sci-paper>/skeleton/CLAUDE.md" ./CLAUDE.md
```

If there **is** one — the common case in an existing project — do not overwrite
it and do not rewrite the author's content. Say what you are about to add, get a
yes, and **append one delimited block**:

```markdown
<!-- sci-paper: begin -->
## Paper workspace (sci-paper)

**Workspace root:** `paper-quenching/` — every path below is relative to it.

**First action, every session:** read `paper/STATE.md` in full, then
`<sci-paper>/skills/_shared/memory.md` and
`<sci-paper>/skills/_shared/house-rules.md`. Those two are the authority on
how to behave here and are deliberately not restated.

| Path | Owner | |
|---|---|---|
| `../analysis/` | author | read, never run |
| `figures/` | author | looked at, never regenerated |
| `notes/` | author | free-form markdown; modified only on an explicit "capture that" |
| `paper/` | agent | the memory: `STATE.md`, `journal.md`, `outline.md`, `open-questions.md`, `lit/` |
| `manuscript/` | shared | the author edits this directly and constantly |
| `.build/` | build | gitignored |

**Build**, from the workspace root:

    (cd manuscript && latexmk -pdf -interaction=nonstopmode -outdir=../.build main.tex)

Keep `-interaction=nonstopmode` or a LaTeX error waits at the interactive `?`
prompt and the build hangs instead of failing.
<!-- sci-paper: end -->
```

Four things about that block:

- **`<sci-paper>` is substituted with the resolved absolute path**, and the
  workspace root with the real directory name. This block is the record of both;
  every later session reads them here instead of resolving them again.
- **The directory map is the one the author actually has.** The `../analysis/`
  row above is the example, not the template: list the paths the survey found,
  relative to the workspace root, and leave out rows for material that does not
  exist. A map describing a layout the author does not have is worse than none.
- **The markers make it re-runnable.** If a block between them is already there,
  replace that block rather than appending a second — it is agent-owned text
  between agent-owned markers. Anything outside them is untouchable.
- **`## `, not `# `.** It is being appended into someone else's document.

If the author would rather their `CLAUDE.md` were not touched at all, the block
goes in `<ws>/paper/CLAUDE-sci-paper.md` and they are told it must be read
manually. Say plainly that this costs the automatic first-action pointer, which
is the whole mechanism this step installs.

### 5c. Wire `.gitignore` at the working-directory root

Cheap and easy to miss. Without it `.build/` and the LaTeX litter get committed.
Append only the lines that are missing:

```sh
touch .gitignore
while IFS= read -r l; do
  [ -n "$l" ] || continue
  grep -qxF "$l" .gitignore || printf '%s\n' "$l" >> .gitignore
done < "<sci-paper>/skeleton/.gitignore"
```

**The list is read from `skeleton/.gitignore`, never retyped here.** It is the
one place the patterns live; a copy in this file is a copy that goes stale the
first time the skeleton gains a line.

`grep -qxF` matches the whole line literally, so `*.log` is not counted as
present because `build.log` is listed. The patterns are unanchored, so they match
at any depth and one `.gitignore` at the working-directory root covers a
workspace at any level. Say what you added.

### 5d. Placeholders

Substitute the paper's short name, the author list, the resolved install path and
the workspace root — **only in the files the copy actually created.** A
`main.tex` that was already there belongs to the author, has no placeholders left
in it, and is not to be rewritten in the name of scaffolding. Say which files you
left alone.

**`\graphicspath` in `main.tex` is the one that bites.** It ships as
`{{../figures/}}`, which is right only when the figures are inside the workspace
root. Where the survey found them somewhere else, set it to that path *relative
to `manuscript/`*: figures in a `plots/` directory beside the workspace root make
it `{{../../plots/}}`. Get this wrong and the first figure inclusion fails the
build with a missing-file error that reads like a broken figure rather than a
broken path.

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
