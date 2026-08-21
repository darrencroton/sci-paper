# Section role: discussion

*What the reader must be able to do after reading it: say why the result
matters, and what would change their mind.*

Real headings for this role in this author's corpus: "Physical models of AGN
feedback", "Interpretation and the implications for galaxy bias", or folded into
"Results and Discussion". The heading rarely says "Discussion".

## The move that defines the role

**Every discussion point traces back to a specific result.** Not to general
knowledge of the field — to something the paper established.

Two different kinds of "traces back" are in play here and confusing them breaks
a house rule. **Rhetorically**, a discussion point refers back to a result the
paper has already shown: "the steep rise seen in Fig. 4". **Scientifically**,
any number or premise in that sentence still carries a `% src:` to the original
note, figure, code or literature note — never to the results section, because
`_shared/house-rules.md` is clear that the draft is not a source. Point the
reader at §3; point the trace at where the number actually came from.

A discussion point with no result behind it is a `\gap{logic}`, stated as such:

```latex
\gap{logic}{no result in this paper supports this — either it needs Fig 6, or it belongs in the introduction}
```

This is the most common way a draft goes wrong, and it is invisible from inside
the draft, because the author knows the supporting fact and does not notice that
the paper never states it.

## The paragraph shape

1. **What we found** — one clause, referring back, not restating the numbers.
2. **What it means physically** — the mechanism, not the restatement.
3. **How it sits against prior work** — *in both directions.* Work that agrees
   and work that disagrees. A discussion that cites only supporting papers is
   the one a referee dismantles.
4. **What would break it** — the alternative explanation, the assumption doing
   the most work, the measurement that would settle it.

## The moves

**Take the alternative explanation seriously.** State it in its strongest form,
then say why it is disfavoured — and if it cannot be ruled out, say that
plainly and open a question. "We cannot presently distinguish between X and Y"
is a publishable sentence and an honest one.

**Do not restate results.** If a paragraph's content is a number and a figure
reference, it belongs in results.

**Calibrate the strength of the claim to what the figure actually supports.**
There is a ladder, and the rungs are not interchangeable:

> is consistent with · suggests · indicates · shows · demonstrates · proves

Pick the rung the evidence reaches and no higher. **Never move a claim up the
ladder while rewriting prose** — if a rewrite makes a claim stronger than the
version it replaced, that is a change to the science and it is flagged to the
author, not made silently.

**Limitations are woven in, not collected.** No paper in this author's corpus
has a Limitations section. The limitation belongs beside the claim it limits,
where the reader meets it at the moment it matters — unless the venue requires
otherwise.

**Distinguish "our model does not include this" from "this does not happen".**
The first is a limitation, the second is a result, and conflating them is how a
modelling paper overclaims.

## Citations

Every comparison to another paper is a real citation or a `\gap{cite}`. Never a
remembered author-and-year. If the claim is "this was first shown by", that is a
priority claim and it needs the actual first paper, which is what
`/paper-lit` snowballing is for.

## What does not belong here

New results. New methods. Anything the reader has not already been shown.
