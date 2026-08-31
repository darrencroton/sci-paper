---
name: paper-voice
description: Distil examples of the author's own writing or style notes, kept in paper-voice/, into a durable per-paper voice profile that /paper-draft and /paper-frame then match by default. Use when the author has put past papers or style notes in paper-voice/ and wants them applied, or wants the profile refreshed after adding something new.
---

# paper-voice

Not a pipeline step. Run this whenever `paper-voice/` has something in it the
author wants applied — typically once, early, but just as validly months into
a project after a second past paper is added.

**What this is not.** Not a style-matching pass that runs on every paper by
default (`_shared/house-rules.md` and Plan §10 are explicit that voice-matching
is opt-in), and not the retired idea of building the author's whole corpus into
the system (Plan §15). This is one paper's own, workspace-local, author-curated
profile — its existence is the opt-in, nothing more.

## Before anything

Work from the workspace root, which `CLAUDE.md` names and
`_shared/house-rules.md` defines; every path below is relative to it.

Read `paper/STATE.md` in full first. Then, from the sci-paper installation
(`../_shared/` relative to this skill):

- `_shared/memory.md`
- `_shared/house-rules.md` — its **Voice** section is what this skill's output
  is for; read it here rather than have it restated.

## 1. Read what is there

```sh
ls -R paper-voice/ 2>/dev/null
```

**The shipped `README.md` does not count as content.** Every fresh workspace
has one — it explains what the directory is for, not what the author's voice
is — so its presence alone is not a signal that the author has put anything
here yet. If the only thing present is that `README.md`, treat it the same as
empty: say so and stop, there is nothing to distil, and creating a profile
from nothing (or from the directory's own instructions to the author) would be
inventing a voice rather than observing one.

Read everything else in it, in full — past papers (PDF, read natively),
freeform notes on style or convention, whatever the author put there. This is read-only
material; nothing here is ever modified, and nothing outside `paper-voice/` is
ever written by this step except `paper/voice.md` itself.

## 2. Distil, with examples

The output is **concrete and quotable, not a list of adjectives.** "Formal but
direct" describes nothing a drafting session can act on; "opens results
paragraphs by stating the finding first, caveats after — *'The bright-end
slope steepens above L\*; this is not significant below 2σ'* — never the
reverse order" does. For each past paper or note read, look specifically for:

- **Sentence and paragraph habits** — typical sentence length, how a paragraph
  opens (claim first, or build-up first), how long a paragraph runs before a
  break.
- **Hedging language** — "we find" vs "it is found that", how confidently a
  result is stated, where a caveat is placed relative to the claim it qualifies.
- **Register** — contractions or not, first person plural or passive voice,
  how technical the vocabulary runs relative to the field's own convention.
- **English variant** — spelling, "-ise" vs "-ize", date and number formatting,
  if it is consistent across what was read.
- **Anything the author's own style notes say directly** — these override
  anything inferred from the papers, since they are the author's explicit
  instruction rather than an observation.

Quote a short real example for each pattern claimed. A profile entry with no
example is exactly the kind of vague prose Plan §13 warns produces generic
output — the whole value of this skill is in how concrete `voice.md` ends up.

**Where the sources disagree** — two past papers use a different register, or a
style note contradicts what the papers actually do — say so in `voice.md`
rather than silently picking one; a drafting session can decide, the profile
should not decide for it.

## 3. Write `paper/voice.md`

Rewritten wholesale each run, not appended to — it reflects whatever is
currently in `paper-voice/`, not a history of past runs.

```markdown
# Voice profile

_Distilled: <date>, from: <what was read in paper-voice/>_

## Sentence and paragraph
<concrete, with a quoted example per pattern>

## Hedging and confidence
<concrete, with a quoted example per pattern>

## Register
<concrete, with a quoted example per pattern>

## English variant
<observed, or stated directly in the author's own notes>

## Disagreements
<where sources conflicted, and that this is left for a drafting session to
resolve rather than resolved here>

## Venue
This paper follows <venue>'s own conventions for referencing style and
document requirements. Where `_shared/venues/<venue>.md` exists, see that —
these are venue rules, not voice, and are not restated here. Where a venue is
chosen but that file does not exist yet (it is a later phase, §9.2), note here
only the venue's name and any convention the author has stated directly; do
not invent or guess the rest.

Where the author's own observed habit and the venue's requirement conflict —
most often English variant — **the venue wins**: it is a submission
requirement, not a style preference, and this profile does not override it.
```

Leave out the **Venue** section entirely if no venue is chosen yet.

## 4. Report back

In conversation: what was read, the handful of patterns that came out of it
concretely enough to be worth stating, and anything the sources disagreed
about. Say plainly that `/paper-draft` and `/paper-frame` will now apply this
by default for the rest of this paper.

## 5. Close the session

Update `paper/STATE.md` and append the `paper/journal.md` entry, per
`_shared/memory.md`.
