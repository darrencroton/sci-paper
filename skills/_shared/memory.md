# Memory protocol

Read this once per session. It is the same for every skill and for ordinary
conversation. It is written here and nowhere else.

A new conversation is continuous with the last one only because these files
exist and get written. That is the whole mechanism.

---

## Three tiers

| File | Read | Lifespan | Holds |
|---|---|---|---|
| `CLAUDE.md` | automatically | stable | **how to behave** — house rules, directory map, venue, build command, the pointer to `STATE.md` |
| `paper/STATE.md` | first action of every session | **only true today** | **where we are** — section status, what is settled, what is open, what to do next |
| `paper/journal.md` | on demand | permanent | **how we got here** — dated entries: discussed, decided, changed, open |

The split test: *will this still be true in three months?* Yes → `CLAUDE.md`.
No → `STATE.md`.

`CLAUDE.md` holds no paper knowledge. Knowledge put there goes stale silently,
because nothing ever prompts a review of it.

---

## First action of every session

Read `paper/STATE.md` in full — all of it, without deciding whether to. It is
capped at two pages precisely so this is cheap.

Then, only as the work requires:

- `paper/outline.md` — whenever the argument or section ordering is in play. It
  is the **sole authority** for the argument.
- `paper/open-questions.md` — whenever a `\gap{q}` or an open decision comes up.
- `paper/lit/index.md` — before any literature search, so the same paper is not
  chased twice.
- `paper/journal.md` — when the question is *why* something is the way it is.
  Search it; do not read it whole.

---

## STATE.md

Living, ≤ 2 pages, **rewritten** each session — never appended to. The cap is
the mechanism: a file that grows past being read reliably is a file that stops
being read at all.

```markdown
# State — <paper short name>
_Last updated: 2026-08-21_

## Argument
See `paper/outline.md` — the single authority. Note here only what is currently
*in flux* about it, not a restatement.

## Sections
| Section | Status | Notes |
|---|---|---|
| Methods | drafted | from code/sam/, 2 gaps |
| Results | partial | Fig 3–5 written; Fig 6 not yet discussed |
| Discussion | sketch | interpretation of the LF cutoff still unsettled |
| Intro / Conclusions | not started | deliberately deferred |

## Settled
- <decision> (<journal date>)

## Open
- <ids into open-questions.md>

## Next
<the one or two things to do next>
```

Every *Settled* line carries the journal date. The date is not decoration: it is
how a later session finds the reasoning, and how a reversal is spotted.

---

## journal.md

Append-only. One entry per working session, written by whichever skill ran —
or by an ordinary conversation that decided something. Never rewritten, never
pruned.

```markdown
## 2026-08-21
**Discussed:** whether the bright-end cutoff needs the AGN model or follows from cooling alone.
**Decided:** keep both, present cooling first — the AGN case is stronger after the reader has seen Fig 4.
**Changed:** rewrote sections/04_results.tex §2; added 3 refs.
**Open:** need the z=2 numbers before the Discussion can close.
```

**When a decision reverses**, the new entry says so explicitly and names the
date it overturns — and **every file holding current truth is brought into
line**: `STATE.md`'s *Settled*, `outline.md` if the argument changed, and the
question's status in `open-questions.md`. Updating only `STATE.md` would leave
`outline.md` — the sole argument authority — stating the overturned position.

Nothing is ever edited in the journal. The correction is the newer entry.

---

## open-questions.md

Three fields, no more: an id, a status with its date, the question.

```markdown
- **Q7** _open_ · 2026-08-21 · Is the 100-particle cut the right one for the morphology claim?
- **Q4** _resolved 2026-08-19_ · Which cosmology to quote → WMAP1; see journal 2026-08-19
```

Ids are referenced from `\gap{q}` markers and from `STATE.md`. Resolved
questions stay in the file — they are the cheapest record of why something is
the way it is.

---

## Literature notes

`paper/lit/index.md` is a flat roster — one row per paper that has entered play,
whether or not it has been read:

```markdown
| Bibcode | Handle | Why it is in play | Read |
|---|---|---|---|
| 2006MNRAS.365...11C | Croton+06 | the radio-mode model we compare against | yes |
| 2015MNRAS.451.2663H | Henriques+15 | later calibration of the same model | no |
```

The *Handle* is what the prose calls the paper. *Why it is in play* is one
clause, and it is the field that stops the same paper being chased twice in
three months' time.

`paper/lit/<bibcode>.md` exists **only for papers actually read in depth**. The
asymmetry is deliberate: a stub file per search hit would be hundreds of empty
files. The filename is the bibcode exactly as ADS writes it, `.md` appended —
`2013ARA&A..51..511K.md`. Bibcodes contain `&` and `.`, which are fine in a
filename but need quoting in a shell.

```markdown
# 2006MNRAS.365...11C — Croton+06

**Read:** 2026-08-21 · [ADS](https://ui.adsabs.harvard.edu/abs/2006MNRAS.365...11C)

## What it does
<two or three sentences: the sample or simulation, the method, the headline result>

## Why it matters here
<what this paper takes from it, or argues against — one paragraph>

## Extracted values
| Value | Where in the paper | Notes |
|---|---|---|
| $M_{\rm crit} = 10^{12.5}\,h^{-1}M_\odot$ | Table 2, row 3 | their $h=0.73$, Chabrier IMF |
| bright-end slope steepens above $L^*$ | Fig. 8 — **visual estimate** | not quoted as a measured value |

## Caveats
<sample limits, cosmology, IMF, mass definition, aperture, resolution — whatever
would make a comparison unfair. Each one names where in the paper it is stated,
the same as a value does: these live in a methods section nobody will find again
without the pointer, and they are what decides whether a comparison is fair at all.>
```

**Every extracted value names where in the paper it came from** — the table and
row, the equation number, the section. That location is what a `% src:` into
this file eventually points at. The visual-estimate rule in
`_shared/house-rules.md` applies to these notes too, and the label is written
here rather than left to be remembered, so that it travels with the number.

---

## Last action of every session

This is the last instruction here because it is the last thing to do, and
because skipping it breaks continuity silently — tomorrow's session cannot tell
that today happened.

1. **Rewrite `paper/STATE.md`** — including its `Last updated` date. Rewrite,
   not append; keep it under two pages by deleting what is no longer true.
2. **Append a dated entry to `paper/journal.md`.**
3. If a decision reversed, apply the reversal rule above to every file.

Do this even for a short session. A session that only answered a question still
answered it.
