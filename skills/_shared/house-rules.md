# House rules

Read this once per session. It applies to every skill and to ordinary
conversation alike. It is written here and nowhere else; skills reference it
and do not restate it.

---

## Division of labour

**The author owns** the science, the notes, the figures, the analysis code,
every claim, every number, every interpretation, and the final text. The author
is the verifier and reads the paper in detail, repeatedly.

**The agent owns** turning notes into prose; literature legwork; keeping the
record of what was discussed and decided; suggesting connections and tensions
the author cannot see from inside the draft; drafting the framing sections from
the established body; assembling the bibliography.

**Never:**

- modify anything already in `notes/`
- run or modify analysis code
- regenerate figures
- silently change the strength of a claim while rewriting prose

**One deliberate exception.** When the author says *"capture that"*, create a
**new** note from what they just said — and only then. The rule exists to stop
unrequested edits to the author's own words, not to force them to type before
they can begin. Existing content is never touched.

---

## Gap markers

The draft is allowed to be incomplete. It is not allowed to hide a hole it
knows about.

One macro, five kinds:

```latex
\gap{number}{cooling threshold — need the value from run 3}
\gap{cite}{who first showed the bright-end cutoff?}
\gap{q}{is this the right sample cut? see paper/open-questions.md (Q7)}
\gap{logic}{this does not yet follow from Fig 4}
\gap{todo}{expand once the z=2 run finishes}
```

Mode is a package option in `main.tex`:

- `\usepackage{astropaper}` — **draft** (the default). Markers render loudly
  inline and in the margin.
- `\usepackage[final]{astropaper}` — **final**. Every `\gap` invocation raises a
  package error and the build fails. A gap-free manuscript builds cleanly.

Switching is a one-word edit and it is visible in the diff.

**Collecting the gaps is a grep, not a tool.** Available at any time, not only
at `/paper-finish`:

```sh
grep -rn '\\gap{' manuscript --include='*.tex'
```

Restricted to `.tex`, because `astropaper.sty` contains the macro's own
definition. Recursive, so it works before `sections/` exists.

**What this guarantees, and what it does not.** It guarantees a *marked* gap
cannot reach a submitted manuscript. It does not catch a free-text `TODO`,
`TBD` or `XXX`, and it cannot catch a number written instead of marked — that
is what the integrity rules below are for.

---

## The two integrity rules

Everything else about verification is the author's. These two are kept because
they are nearly free and they protect the author at the moment they are reading
fast.

### Rule 1 — every quantitative statement is either traced or marked

A number, range, threshold or uncertainty in the manuscript carries exactly one
of:

- a `% src:` comment naming where it came from, or
- a `\gap{number}` marker, if it has no source yet.

There is no third option. **Never write a number that cannot be traced.** The
same applies to a citation: found and cited, or `\gap{cite}`.

**The legitimate sources are wider than the notes**, because in practice a
result lives wherever the author put it:

| Source | Anchor |
|---|---|
| a note | `% src: notes/methods.md "cooling threshold"` |
| a figure the agent looked at | `% src: figures/fig3.pdf` |
| a line in the analysis code | `% src: code/plot_lf.py:88 (fit_break)` |
| a module-level constant in that code | `% src: code/plot_lf.py:12 (MSTAR_MIN)` |
| a literature note | `% src: paper/lit/2020MNRAS.499.5732S.md table 2` |

A figure or a line of code is a first-class source. Marking the author's own
figure-derived result as unknown because it is not written down in a note is a
worse failure than any it prevents.

**The draft is never a source.** `notes/`, `figures/`, `code/`, the author's
tables and `paper/lit/` are where science comes from. A number or claim already
in the manuscript is never evidence for another one: that is circular, and it is
how a transcription error propagates.

**A value read off a figure is an estimate and is labelled as one** — the
author's own figures as much as published ones. An exact value must trace to a
note, a table, an explicit annotation, or the code or data behind the plot.
Prose that quotes a point read off a plot to three significant figures is false
precision no matter how good the trace looks.

**Copy units and $h$-scalings exactly as the source writes them, and record
which convention the source used. Never convert.** A comparison silently made
between $h^{-1}M_\odot$ and $M_\odot$ is the commonest way a comparison goes
wrong, and it survives every proofread because both numbers are correct. The
same holds for an IMF, a cosmology and an aperture: they travel with the
number or the number is not usable.

**Code is read, never run.** A `% src:` anchor into `code/` points at a
definition or a literal in the source; it never means anything was executed. A
result that exists only as the *output* of a run, written down nowhere, has no
source yet — it is a `\gap{number}` until the author records it.

### Rule 2 — BibTeX comes verbatim from ADS

Never hand-written, never adjusted, never "corrected". `tools/ads.py export` is
the sole supported path to a `refs.bib` entry.

### Both rules are hard instructions, not gates

Nothing structurally prevents an agent with write access to `refs.bib` from
composing an entry, or from writing an untraced number. These rules make the
wrong thing visible; they do not make it impossible. That is the honest
description and it is the right one — the author is the verifier.

---

## Source comments

The `% src:` comment is the entire traceability mechanism. There is no
registry, no database, no index.

```latex
% src: notes/methods.md "cooling threshold"
```

Invisible in output, greppable, zero ceremony. Two rules about form and scope:

**Anchor by name, not by line number.** `notes/` is author-owned and edited
constantly; inserting one paragraph invalidates every line pointer below it,
and a link known to be stale is a link that gets ignored. Anchor on a heading
or a short distinctive quoted phrase. Code is the one exception where a line
number is useful, and it carries alongside it the **symbol that owns the line**
— the enclosing function where there is one, and the constant's own name where
the line is a module-level literal, which is where analysis scripts keep their
load-bearing cuts more often than not. The symbol is what survives the edit that
moves the line.

**Write a code line number by looking at the file, never from memory of it.**
Adding an import or a docstring line shifts every anchor below it silently, and
an anchor that is off by two points at real code, which is exactly why nobody
catches it.

**Comment what is load-bearing, not everything.** Every quantitative statement
(required by rule 1), plus method and sample definitions and any unusually
load-bearing claim. Connective and qualitative prose gets nothing — commenting
every sentence buries the section diffs and devalues the marks that matter.

---

## Non-destructive editing

The author edits `manuscript/` directly and constantly. That is the point of
the project.

**Edit in place and preserve author prose.** Never regenerate a section
wholesale over existing text without showing what would be replaced and being
told to go ahead.

A single silent overwrite of a day's hand-editing ends the author's trust in
the system permanently, and git making it *recoverable* does not make it
acceptable.

The same applies to `paper/`: `journal.md` is append-only, and `STATE.md` is
rewritten deliberately, not clobbered.
