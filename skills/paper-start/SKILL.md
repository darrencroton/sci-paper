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

First, look whether there is anything to resume. A workspace is always
`sci-paper-workspace*/`, so glob for it — from inside one, or from the working
directory above:

```sh
ls paper/STATE.md 2>/dev/null                       # already inside a workspace
ls sci-paper-workspace*/paper/STATE.md 2>/dev/null  # at the working directory
grep -l 'sci-paper: begin' CLAUDE.md 2>/dev/null
```

**If any of these finds something, this is not a new paper for this project** —
though it may still be a new paper sharing an existing project with one that
already has a workspace. **Stop here: §1–§5 do not run.** Read the matching
`paper/STATE.md` in full before anything else, exactly as every other session
does, then the shared files below, then ask what the author wants re-ingested
before touching a thing. Where more than one workspace exists, resolve which
one per `_shared/house-rules.md`'s **The workspace root** before reading
anything.

**If none of these finds anything, this is the one session in the project with
no state to read** — and the only one where the shared files come first.

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

`_shared/house-rules.md` has the rule: the workspace root is always
`sci-paper-workspace/`, isolated in its own git repository, never `.` and never
proposed or chosen. There is exactly one decision to make, and only if the
survey (or the resume check above) shows one already exists:

- **No existing `sci-paper-workspace*/` here** → the name is `sci-paper-workspace`,
  full stop. Nothing to ask.
- **One already exists, and this is a second, distinct paper** → ask for a
  short, distinguishing suffix and use `sci-paper-workspace-<suffix>/`. Say why
  in one sentence — the `.gitignore` glob below already covers this variant
  with no further edit needed.

Whichever it is, it is written `<ws>` from here on. Create it, its own git
repository, and the working directory's exclusion of it, **in that order and
immediately** — a gap between "the workspace exists as a repository" and "the
working directory ignores it" is a window in which an ordinary `git add -A` in
the working directory could stage the whole workspace as an embedded
repository. Never a first commit inside `<ws>` itself, which stays the
author's decision like any other repository:

```sh
mkdir -p "<ws>"
(cd "<ws>" && git init -q)
touch .gitignore
grep -qxF 'sci-paper-workspace*/' .gitignore || printf 'sci-paper-workspace*/\n' >> .gitignore
```

§5c revisits this same `.gitignore` line only to say what was added and why it
is a glob; it is not a second write.

From this point on, `<ws>` is the working directory for every remaining step
in this skill: `paper/`, `manuscript/` and every bare path below refers to
`<ws>/paper/`, `<ws>/manuscript/`, and so on — either `cd` into `<ws>` for the
shell steps that follow, or prefix each path with it, but resolve every one of
them, since a bare write from here on that lands outside `<ws>` is exactly the
isolation failure this design exists to prevent. `notes/`, `figures/`, `code/`
and `data/` are the one deliberate exception: they are the author's own,
outside `<ws>`, and stay addressed relative to the working directory as the
survey found them.

Nothing the author owns moves into `<ws>`, then or later.

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
and only those, get converted first — into `<ws>/.build/`, never into the
working directory, since `.build/` is a workspace artefact (§4.2) and `<ws>`
already exists by this point (§1a):

```sh
mkdir -p "<ws>/.build"
gs -q -dNOPAUSE -dBATCH -dEPSCrop -sDEVICE=png16m -r150 \
   -sOutputFile="<ws>/.build/fig3.png" figures/fig3.eps
```

`figures/fig3.eps` here is the illustrative case — substitute wherever the
survey in this step actually found it, which is normally the working
directory but is whatever the author's project calls it and wherever it
already lives.

`-dEPSCrop` is not decoration. Without it `gs` paints the figure onto a default
page and hands back a mostly blank US-Letter image with the plot small in one
corner — worse than an error, because it still looks like a figure. The line
assumes a single-page EPS, which is what a plotting library writes; for a
multi-page PostScript file put `%d` in the output name
(`-sOutputFile="<ws>/.build/fig3-%d.png"`), drop `-dEPSCrop`, and look at each
page.

Rasterising a *built manuscript page* is a different job, done later from
inside the workspace once it exists, and does need
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
for f in "<ws>/manuscript/main.tex" "<ws>/manuscript/scipaper.sty"; do
  [ -e "$f" ] && printf 'pre-existing: %s\n' "$f"
done
cp -Rn "<sci-paper>/skeleton/workspace/." "<ws>/"
mkdir -p "<ws>/manuscript/sections"
```

Every part of that earns its place:

- **`skeleton/workspace/.` mirrors the workspace root exactly** — its
  `paper-voice/`, `paper/`, `manuscript/`, `CLAUDE.md` and `.gitignore` all land
  directly in `<ws>/`, because that is the whole point of the skeleton being
  laid out that way. `skeleton/root/` is a different template for a different
  destination and §5b/§5c place it instead.
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

**The author's `notes/`, `figures/` and `code/` are found, not placed, and go
outside `<ws>` entirely** — `_shared/house-rules.md` is the authority. Use them
wherever the survey found them, under whatever they are already called. Create
them **only** for material that exists nowhere, and even then in the working
directory, never inside `<ws>`:

```sh
# only for those the survey found nothing for, anywhere
mkdir -p notes figures
```

Never move or copy the author's existing material to make the layout match a
diagram.

### 5b. Wire the working-directory `CLAUDE.md` index

**The workspace's own `CLAUDE.md` is already done** — §5a's wholesale copy of
`skeleton/workspace/.` placed it at `<ws>/CLAUDE.md` along with everything
else; there is nothing further to do for it here beyond filling its
placeholders at §5d. This step is only about the **working-directory**
`CLAUDE.md`, which is a different file with a different job: an index,
nothing more. Skip it and a session starting at the project root has no way to
find the workspace, even though the workspace itself is fully wired.

If there is **no** `CLAUDE.md` at the working directory, copy the skeleton's
and fill in `<ws>`'s row:

```sh
cp -n "<sci-paper>/skeleton/root/CLAUDE.md" ./CLAUDE.md
```

If there **is** one — the common case in an existing project — do not overwrite
it and do not rewrite the author's content. Say what you are about to add, get a
yes, and **append one delimited block** (or, on a later run with the block
already present, **upsert just this workspace's row** — never rewrite the whole
block, which would drop another paper's entry):

```markdown
<!-- sci-paper: begin -->
## sci-paper workspaces in this project

| Workspace | Short name |
|---|---|
| `sci-paper-workspace/` | quenching |

Each workspace directory above is its own git repository and carries its own
`CLAUDE.md` with the full detail — build command, directory map, install path,
the pointer to `paper/STATE.md`. Read that once inside the relevant workspace;
this index exists only so a session starting here, at the project root, knows
which sci-paper workspaces exist and what to call them.
<!-- sci-paper: end -->
```

**`sci-paper-workspace/` and `quenching` are both substituted** — the row
holds `<ws>`'s real directory name (including the `-<suffix>` if this is a
second paper) and the short name the author gave this one, never the literal
example text above. This block is the record of both; a later session reads
them here instead of asking again.

Three more things about that block:

- **The markers make it re-runnable, and re-running never means rewriting.** A
  second `/paper-start` in this project adds or updates its *own* row; it never
  replaces the table wholesale, or the first paper's entry disappears.
- **`## `, not `# `.** It is being appended into someone else's document.
- **The short name is what a session or a skill matches on, never the directory
  name** — `_shared/house-rules.md`'s **The workspace root** is the authority,
  because the directory can be renamed by hand at any time.

If the author would rather their `CLAUDE.md` were not touched at all, the index
entry goes in `<ws>/paper/CLAUDE-sci-paper.md` instead and they are told it must
be read manually. Say plainly that this costs the automatic pointer a session
starting at the project root would otherwise get.

### 5c. The `.gitignore` situation, both of them

**Both are already done, and deliberately not here.** The working directory's
`sci-paper-workspace*/` line was written at §1a, in the same breath as
creating `<ws>` and its own repository — not later, so there is never a moment
where `<ws>` is a git repository the working directory could accidentally
stage. The workspace's own `.gitignore` (build-artefact lines) was placed at
`<ws>/.gitignore` by §5a's wholesale copy. Say what was added, for both, here
if it was not already said at §1a.

**A glob, deliberately, not the literal directory name**, for the working
directory's line — it is what keeps the isolation covered after a later
rename, or when a second, differently-suffixed workspace is added, with no
further edit to this file ever required.

### 5d. Placeholders

Substitute the paper's short name, the author list and the resolved install
path — **only in the files the copy actually created.** A `main.tex` that was
already there belongs to the author, has no placeholders left in it, and is not
to be rewritten in the name of scaffolding. Say which files you left alone.

**`\graphicspath` in `main.tex` is the one that bites.** It ships as
`{{../../figures/}}` — two levels up from `manuscript/`, through the workspace
root and out into the working directory, which is where the survey normally
finds `figures/` now that the workspace is always its own subdirectory. Where
the survey found figures somewhere else, set the path *relative to
`manuscript/`* to match: the first two `../../` always get from `manuscript/`
back out to the working directory, exactly as in the default, and anything
after that descends from there to wherever the survey actually found
`figures/` — a `plots/` directory nested one level *inside* the working
directory, at `<working directory>/analysis/plots/`, makes it
`{{../../analysis/plots/}}`, not a third `../`, which would instead climb
*above* the working directory. Get this wrong and the first figure inclusion
fails the build with a missing-file error that reads like a broken figure
rather than a broken path.

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
- mention `paper-voice/`, once, briefly — if the author has past papers or
  style notes they want this one to sound like, they can drop them there and
  run `/paper-voice` whenever they are ready. Not a gate, not asked about again.

## 10. Close the session

Write `paper/STATE.md` and append the `paper/journal.md` entry, per
`_shared/memory.md`. `STATE.md`'s *Next* names the next section to draft.
