---
name: paper-draft
description: Write or rewrite one section of the manuscript from the author's notes, figures and analysis code, marking every hole rather than smoothing it over. Use when asked to draft, write, extend or rewrite a methods, results or discussion section. Introduction, Conclusions and Abstract go to paper-frame instead.
---

# paper-draft

`/paper-draft <section>` — write one section into `manuscript/sections/`.

The output is a **deliberately incomplete** section, written under the
traceability and gap rules in `_shared/house-rules.md`. A section that reads as
finished when it is not is the failure mode this skill exists to avoid.

## Before anything

Read `paper/STATE.md` in full first — it is the first action of every session,
and nothing here changes that. Then, from the astro-paper installation
(`../_shared/` relative to this skill; the paper repo's `CLAUDE.md` names the
install path if that does not resolve):

- `_shared/memory.md`
- `_shared/house-rules.md`

Then `paper/outline.md`. They are the authority and are not restated here.

**Introduction, Conclusions, Abstract and Title are not this skill.** They are
`/paper-frame`, which has the technique for writing them from an established
body. If asked for one, say so and offer to run that instead.

## 1. Resolve the section

Find the section in `outline.md`'s Sections table. Take its **role** and its
**heading** — the heading being whatever this paper actually uses.

**This skill drafts the `methods`, `results` and `discussion` roles only.** A row
whose role is `framing` is an Introduction or a Conclusions section: hand it to
`/paper-frame` and say so, rather than looking for a rhetorical-moves file that
does not exist for it.

If it is not in the outline, do not guess: propose a row, get agreement, add it.
The outline is the sole authority for the argument and a section that is not in
it has no place in the argument yet.

Then read `_shared/sections/<role>.md` for each role the section carries. The
role cell holds bare words joined by ` + ` where a section carries more than
one, so a combined "Results and Discussion" reads `results + discussion` and you
read both `results.md` and `discussion.md`. The words *are* the filenames, which
is why nothing else belongs in that cell. Those files hold the rhetorical moves;
this file holds the procedure, and all of them apply at once.

## 2. If the file already exists — stop and look

The author edits `manuscript/` directly and constantly. That is the point of the
project.

- **Extending or filling gaps** → edit in place. Normal case, no ceremony.
- **Restructuring or rewriting over existing prose** → show what would be
  replaced and what it would become, and get agreement first.

Never regenerate a section wholesale over author text; `_shared/house-rules.md`
says why, and it is the authority.

Read the existing section before writing a word of the new one — including the
`% src:` comments, which say what has already been traced, and the `\gap`
markers, which say what was already known to be missing.

## 3. Gather the sources

Science comes from `notes/`, `figures/`, `code/`, any standalone tables the
author keeps, and `paper/lit/`. Those are the only places a number or a claim
may originate. **A table row is among the best sources there is** — better than
a value read off a plot — and it is anchored like any other, by the table and
the row rather than by a line number.

**Read the manuscript's existing sections too** — a section being drafted has to
sit in a paper, and a discussion cannot refer back to a result it has never
read. Read them for what the paper has already established, what wording and
notation it already uses, and what it has already said so this section does not
repeat it.

**But the draft is never a source** — `_shared/house-rules.md` says why. Keeping
those two apart is the whole point. Point the *reader* back at the paper's
results section; point the `% src:` at the note, figure or line of code the
number actually came from. Never at the results section.

The sources behave differently, and it is worth knowing how before writing:

**From notes** — the normal case. The prose follows the author's stated
understanding. Anything the notes do not settle becomes a gap. Anchor by a
heading or a short distinctive quoted phrase, never a line number.

**From code** — mainly for methods. Read the source; write what the code *does*.
Never run it. Anchor with the line and the symbol that owns it — the enclosing
function where there is one, `% src: code/plot_lf.py:88 (fit_break)`, and the
constant's own name where the source is a module-level literal,
`% src: code/plot_lf.py:12 (MSTAR_MIN)`. Analysis scripts keep their
load-bearing cuts at module scope more often than not, and an anchor with no
symbol at all is the one that goes stale unnoticed.

> **Where the code and the notes describe the method differently, write
> `\gap{q}` and open a numbered question.** Do not choose between them. This is
> the one place the agent is genuinely well-placed to catch something the author
> would miss, and it costs a sentence.

**From figures** — look at the figure and describe what is actually plotted, then
check that against the caption, the notes, and the code that made it. A mismatch
between any of them is a `\gap{q}` and a numbered question, never a silent
resolution in favour of whichever seemed most likely.

PDF and PNG are read directly. EPS and PS go through `gs` into `.build/` first,
as `/paper-start` step 3 shows — `pdftoppm` does not read EPS and simply fails
on one.

The visual-estimate rule in `_shared/house-rules.md` applies with full force
here: a value read off a plot is written as an estimate, and an exact value has
to come from a note, a table, an annotation, or the code behind the plot.

## 4. Write

Into `manuscript/sections/NN_slug.tex`, where `NN` is the outline's section
number, zero-padded, and `slug` is the heading reduced to lowercase words joined
by underscores — nothing else. `03_quenching_of_satellites.tex`, not
`03_The Quenching of Satellites.tex`, and never a slash: a combined "Results and
Discussion" is `03_results_and_discussion.tex`. Headings in this project are
whatever the paper actually uses, so they contain spaces, punctuation and the
occasional maths; the filename does not inherit any of it. The heading the
reader sees lives in the `\section{}` line, not in the path.

- A `% src:` comment sits on the line **immediately before** the sentence it
  justifies, so the pairing survives reflowing and shows up in the diff next to
  the prose it belongs to.
- Comment what is load-bearing, in the scope `_shared/house-rules.md` sets:
  every quantitative statement, plus method and sample definitions **and any
  unusually load-bearing claim** — including a qualitative one. The headline
  sentence of a results section is load-bearing even when it carries no number.
  Connective prose gets nothing.
- **Captions carry claims too.** A quantitative or load-bearing statement in a
  `\caption` obeys the same rule as one in the body; a caption is where an
  untraced number most easily hides.
- Match the conventions the manuscript already uses — figure macro
  (`\includegraphics` vs a `\plotone`-style wrapper), citation commands, label
  naming. Do not introduce a second convention.
- Every float gets a `\label` and is `\ref`'d where it is discussed.
- **Figure formats.** `pdflatex` includes PDF, PNG and JPG; it cannot include
  EPS or PS. Where a figure exists only as EPS/PS: first look for a sibling in
  an includable format and check it is the *same plot* — a `_old` or `_v2`
  sibling is often a different one, and this directory is normally untidy.
  Otherwise convert it once, alongside the original, and say that you did:

  ```sh
  gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dEPSCrop \
     -sOutputFile=figures/fig.pdf figures/fig.eps
  ```

  Never overwrite an author figure, and never choose between two versions of one
  figure without asking which is current.
- Copy units and $h$-scalings exactly as the source writes them. Never convert.
- Write the gap markers as you go, with a note that says what would fill them —
  `\gap{number}{need the value from run 3}`, not `\gap{number}{TBD}`.

Any `\gap{q}` gets a matching entry in `paper/open-questions.md`, and the marker
names its id.

## 5. Read every trace back before you build

The traces are the product. A `% src:` that points at the wrong place is worse
than no trace at all, because it converts an unchecked claim into one that looks
checked — and the author reading fast is exactly who it fools.

So, once the section is written and before it is wired in, go back over it:

- **Re-open every source you cited and read the claim back out of it.** Not from
  memory of having read it, and not from the draft — from the file, the figure
  or the table. Code line anchors in particular are written from the open file,
  per `_shared/house-rules.md`.
- **Check the direction of every comparison.** Above or below, steeper or
  shallower, rises or falls. A reversed comparison is the single easiest thing
  to write, the hardest to see on re-reading, and it will carry a perfectly
  valid-looking trace.
- **Check that a figure and the code said to have made it actually agree.** Not
  the axis label alone — the legend text, the number of curves, the guide lines,
  the tick range. A script that would round a label differently, or that draws
  none of the annotations the figure shows, did not make that figure, and citing
  it as though it had is a false trace of the worst kind: it looks like the
  strongest evidence in the section. Where they disagree, the figure is what the
  reader sees, so trace displayed values to the figure and raise a `\gap{q}`
  asking which artefact is current.
- **Check that the named symbol is the one that does the work.** A constant
  belongs to the line that defines it, not to the function that happens to use
  it; a sample cut belongs to the function that applies it.
- **Sweep for the untraced, and do not sweep only for digits.** Every
  quantitative statement carries a `% src:` or, where it has no source yet,
  specifically a `\gap{number}` — a `\gap{q}` records a decision the author
  owes, and does not discharge a missing value. Quantities hide in words as
  readily as in numerals: *four* snapshots, a *factor of two*, *twice* as steep,
  *half* the sample, an *order of magnitude*. A grep for digits will not find
  any of them, so read for them. The same applies to a quantitative or
  load-bearing claim in a `\caption` — not to every caption indiscriminately,
  which would bury the marks that matter.

Anything that does not survive this pass becomes a `\gap`, not a softer
sentence. This is the one step in the skill that cannot be delegated to the
build: `latexmk` will happily compile a confident falsehood.

## 6. Wire it in

Uncomment or add the `\input` line in `manuscript/main.tex`, in outline order.
It must name **the file just written** — the skeleton ships commented
placeholders like `\input{sections/03_results}`, and uncommenting one of those
instead of pointing at `03_quenching_of_satellites` is a file-not-found the
build will catch a step later for no reason.

## 7. Build and report

```sh
(cd manuscript && latexmk -pdf -interaction=nonstopmode -outdir=../.build main.tex)
grep -rn '\\gap{' manuscript --include='*.tex'
```

The parentheses are load-bearing. A bare `cd manuscript && latexmk ...` leaves
the shell inside `manuscript/`, so the gap grep on the next line looks for
`manuscript/manuscript`, finds nothing, and reports a clean draft with every gap
still in it.

`-interaction=nonstopmode` is not optional in a session. Without it a LaTeX
error stops at the interactive `?` prompt and the build hangs until it is
killed — and in `final` mode, where every `\gap` raises an error deliberately,
that is the *normal* path rather than an unlucky one.

The `.log` is the authority on undefined references and missing figure files —
do not re-derive it. Report:

- the section, and roughly what it now says
- **every gap, by kind, with what would fill it** — this is the main output, not
  an appendix to it
- anything the sources disagreed about
- whether it compiles

If the build fails, fix what *this* edit broke — a missing `\input`, a stray
brace, an unconverted figure — and report. An honestly incomplete draft still
has to compile.

But a build failure is not a licence to edit around the house rules. Where
fixing it would mean changing author prose that was already there, choosing
between two versions of a figure, or deciding something scientific, stop and say
so: report the failure, name what would fix it, and still close the session.
A compiling draft bought by quietly overwriting the author's paragraph is a
worse outcome than a broken build.

## 8. Close the session

Update `paper/STATE.md` (this section's row, and *Next*) and append the
`paper/journal.md` entry, per `_shared/memory.md`.
