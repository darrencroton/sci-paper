# Section role: methods

*What the reader must be able to do after reading it: select the same sample and
re-derive the same numbers.* Not "understand the approach" — reproduce it.

No paper in this author's corpus uses a "Methods" heading. Real ones are "The
dark matter skeleton: the Millennium Run", "The Galaxy Formation Model",
"Count-in-Cells Statistics". Take the heading from `paper/outline.md`; take the
*moves* from here.

## Order

Data → sample → measurement → model → what is held fixed. Each step should be
answerable without reading ahead.

## The moves

**Every cut carries a number and a reason.** "We select galaxies above
$10^9\,M_\odot$" is half a sentence. The reason — resolution limit, completeness
limit, a signal-to-noise floor, matching a previous sample — is what lets the
reader judge it, and it is what a referee asks for. If the notes give the
threshold but not the reason, write the threshold and mark the reason
`\gap{q}`; do not invent a plausible justification.

**Cosmology and the $h$-convention are stated once, explicitly, and never
converted.** This author's own published tables carry three different powers of
$h$ ($+3$, $-1$, $-3$) plus a $5\log_{10}h$ magnitude convention in a single
header, with the cosmology declared in the *table caption* rather than in the
methods text. So: find where the convention is actually declared — notes, code,
a figure axis, a table caption — trace it with `% src:`, and state it here as
well. **Copy units and $h$-scalings exactly as the source writes them. Never
rescale a number to a different convention**, even when the arithmetic looks
trivial; that is a science decision and it is the author's.

**Name the software and the version.** Halo finder, merger-tree builder,
photometry pipeline, fitting library, simulation code. A version that is not
written down anywhere is `\gap{number}`, not an omission.

**The checklist depends on what kind of paper it is:**

- *Simulation* — box size, particle number and mass, force softening, snapshot
  count and spacing, cosmological parameters, halo finder, tree construction,
  and which physics is switched on.
- *Observation* — survey and data release, sky area, magnitude or flux limits,
  completeness, redshift range and its determination, and the selection function.
- *Model / semi-analytic* — the free parameters, what they were tuned against,
  and what was held fixed. "Tuned to the local luminosity function" is a
  load-bearing claim and needs a `% src:`.
- *Method / pedagogical* — the corpus contains one paper with eight sections and
  no Results at all. Where the paper *is* the method, this role carries the
  whole argument and `results.md` may not apply.

**Tense.** Past for what was done ("we selected", "the simulation was run"),
present for what the code or the model does ("the cooling rate scales as").

## Drafting from code

The strongest case for this role, and the one place the agent is genuinely
well-placed to catch something.

Describe **what the code does**, not what it is named or what the notes claim it
does. Anchor it as `_shared/house-rules.md` specifies — code is the one place a
line number is used, and it carries the symbol that owns the line.

The code-versus-notes conflict rule matters more in this role than in any other,
because this is the role written from code: it is exactly how a wrong database
column reaches a published figure.

Read, never run. A constant in the source is a source — and in an analysis
script the load-bearing ones are usually sitting at the top of the file, above
any function. A number that only exists as the output of a run, written down
nowhere, is `\gap{number}`.

## What does not belong here

Results. Motivation. Comparison to other work. If a methods paragraph is arguing
for something, it belongs in discussion.
