# Section role: results

*What the reader must be able to do after reading it: say what was measured and
how strongly, without having been told what it means.*

## The paragraph shape

One result per paragraph, in this order:

1. **Point at the figure or table first**, not last. `Figure~\ref{fig:lf} shows…`
   The reader is looking at it while they read the sentence, not after.
2. **State what is seen**, in the plainest available words.
3. **Quantify it** — the number, the range, the slope, the significance. This
   sentence carries a `% src:` or a `\gap{number}`; there is no third option.
4. **Say where it stops being true** — the bin where the statistics run out, the
   mass above which resolution bites, the redshift beyond which the sample is
   incomplete. A result with no stated limit reads as an overclaim even when it
   is not one.

Interpretation is deferred. If `paper/outline.md` says this paper uses a
combined "Results and Discussion" — as one in this author's corpus does — then
read `discussion.md` as well and interleave deliberately, one result then its
interpretation, rather than blurring the two throughout.

## The moves

**Never state a result the figure does not show.** The most common failure is a
sentence that is true, supported by the notes, and simply not visible in the
figure it cites. Either point at the thing that does show it, or say it without
the figure reference.

**What the visual-estimate rule looks like here.** "The break sits near
$M_\ast \simeq -21$" is honest; "$M_\ast = -20.94$" read off the same plot is
false precision, however good the trace looks.

**Check the axis label against what is actually plotted.** In this author's
corpus a mislabelled axis — $V_{\rm max}$ plotted, $V_{\rm vir}$ labelled,
because the wrong database column was loaded — produced a wrong published
conclusion in a paper with thousands of citations, caught only after publication
by an outside reader. When the figure, its caption, the code that made it, and
the notes do not all say the same thing, that is a `\gap{q}` and an entry in
`open-questions.md`. It costs a sentence to raise and it is the single most
valuable thing this role does.

**Comparison to previous work is a fact here, an argument in discussion.** "This
is steeper than the slope reported by \citet{X}" belongs in results. Why the two
disagree does not.

**Report the caveat that travels with the measurement** — scatter, the number of
objects in the extreme bin, error bars that are Poisson rather than
cosmic-variance. Put it in the same paragraph as the number. A caveat collected
into a paragraph at the end of the section is a caveat the reader skips.

**Order results by the argument, not by the order the figures were made.**
`paper/outline.md` sets the order. If the outline's order and the figure
numbering disagree, say so and ask — do not silently renumber the author's
figures.

## Figures and tables

Every float gets a `\label` and is `\ref`'d from the text at the point it is
discussed. Match the figure-inclusion macro the manuscript **already uses**:
half this author's papers wrap `\psfig` in `\plotone` and contain no
`\includegraphics` at all. Introducing a second convention into a manuscript
that already has one is a diff the author has to undo.

A number quoted from a table is traced to the table, not to the sentence
elsewhere that also quotes it.

## What does not belong here

Physical explanation, implications, comparison arguments, limitations of the
model as opposed to limits of the measurement. Those are discussion.
