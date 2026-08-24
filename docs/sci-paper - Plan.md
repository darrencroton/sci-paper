# sci-paper — Plan

**Version:** 2.0
**Date:** 2026-08-22
**Author:** Darren Croton (Swinburne), with Claude Opus 5
**Status:** P1–P3 built and validated · P4 next

> **This document is the specification and the build record.** §1–§13 are the design and are the authority on what gets built. §14–§16 record what has actually been built, what was verified and how, which decisions are settled, and how the system is installed. There is no separate status document: if something matters and is durable, it is here.

> **Revision history.**
> **v1.0** (2026-08-21) — first design after the superseded v5.1 project was abandoned.
> **v1.1** — external panel round 1 (`codex`/gpt-5.6-sol and `opencode`/opencode-go/hy3, read-only, high effort, staggered starts). No P0. Both independently found the same worst defect: §6.2's number rule forbade the very figure- and code-derived values that §7.2 makes first-class drafting sources. Fixed by unifying traceability into one rule. Also fixed: the draft could overwrite the author's own edits; `outline.md` and `STATE.md` both claimed the argument; `% src:` used fragile line anchors; `/paper-frame` used a soft status as a hard gate; the gap guarantee was overclaimed; the `.sty` final-mode trigger was ambiguous; venue conformance was asserted with no mechanism.
> **v1.2** — panel rounds 2 and 3. Added the "capture that" exception to the never-edit-notes rule (§3), widened the legitimate `% src:` sources, and settled the `article`-class default when no venue is chosen. This revision was mislabelled `1.0` in its own header, which is how it came to be found.
> **v2.0** (2026-08-22) — the build record folded in, and one design change. §11 carries per-phase status and evidence; §14 the validation record; §15 the settled decisions and the approaches already declined; §16 installation. The two supporting evidence documents (`Corpus Evidence.md`, `Ecosystem Research Record.md`) were retired to the local, untracked `docs/archive/`: every judgement they still supported is now stated here directly, so nothing in this plan depends on reading them.
> The design change is §4.1, the **workspace root**. Preparing the system for global installation exposed the assumption that the working directory *is* the paper — so in a real project directory `/paper-start` skipped the existing `CLAUDE.md` and `.gitignore` rather than merging into them, and left the workspace looking scaffolded while nothing pointed a session at `paper/STATE.md`. The paper now scaffolds into a named subdirectory of the working directory by default, with the root `CLAUDE.md` and `.gitignore` appended to. The layout *inside* the workspace is unchanged, so P1–P3 remain valid; §14.2 records that the new path is specified and not yet dogfooded.

> **Relationship to earlier work.** This supersedes an earlier design that solved a different problem: mechanically verifying a finished manuscript's integrity via approval registries, gates and deterministic checkers. On author direction that project is abandoned. The author is the verifier and reads the paper in detail, repeatedly. What is needed instead is a **writing collaborator with durable memory and a strong literature arm**. Why that design was abandoned rather than trimmed is in §12 and §15.

---

## 1. What this is

A small set of Claude Code skills that take an astronomer's **notes, figures, tables and analysis code** and produce a **deliberately incomplete first draft** of a journal paper — holes marked, not smoothed over — and then support months of iteration on that draft: suggesting connections, searching the literature, finding supporting and contradicting work, filling references, and finally writing the Introduction and Conclusions once the body has something to introduce and conclude.

It is designed for the way papers are actually written: **starting before the picture is complete, and letting the writing shape the result.**

The system must work equally well at both ends of that journey — a pile of half-formed ideas and three figures at one end, a settled argument needing polish and references at the other.

## 2. Design principles

1. **KISS.** The first version ticks the high-level boxes and nothing more. Complexity is added only when its absence has actually caused a problem, not when it is imagined it might.
2. **DRY.** Every rule, format and convention has exactly one home. Skills reference shared files; they do not restate them.
3. **Don't rebuild what the harness gives you.** Reading files, grep, glob, bash, PDF reading, image viewing, subagents and git are already there. Custom code must earn its existence against them.
4. **The author is the gate.** The system never claims a number, method or citation is correct. It makes what it did *visible and traceable* so the author can check it fast.
5. **Honest incompleteness.** A gap is marked explicitly and loudly. The draft is never allowed to hide what it does not know.
6. **Memory is a feature, not a side effect.** Every session ends by writing down what happened. Every session begins by reading it.
7. **Ordinary technology.** Markdown, LaTeX, git, and one small stdlib Python script. No MCP servers, no databases, no schemas to validate, no state machines.

## 3. Division of labour

**The author owns:** the science, the notes, the figures, the analysis code, every claim, every number, every interpretation, and the final text.

**The agent owns:** turning notes into prose; literature legwork; keeping the record of what was discussed and decided; suggesting connections and tensions the author cannot see from inside the draft; drafting the framing sections from the established body; assembling the bibliography.

**Two hard rules** (§6.2) — every quantitative statement is either traced to a legitimate source or marked as a gap, never guessed; BibTeX is exported verbatim from ADS, never composed.

**Never:** modify anything already in `notes/`; run or modify analysis code; regenerate figures; silently change the strength of a claim while rewriting prose.

**One deliberate exception.** Often the most natural way to start is to talk the idea through rather than to write it down first. When the author says *"capture that"*, the agent may create a new note from what they just said — and only then. The rule exists to stop unrequested edits to the author's own words, not to force them to type before they can begin. Existing content is never touched.

---

## 4. Workspace layout

The system is installed once (§16). Each paper gets a **workspace** scaffolded by `/paper-start`.

### 4.1 The workspace root

A paper is almost never written in an empty directory. The normal case is an existing science project — data, analysis code, its own git repo and often its own `CLAUDE.md` — into which a paper is now being written. So the workspace is **a named subdirectory of the working directory**, and every path the skills use is relative to that subdirectory, called the *workspace root*.

```
my-project/                      # the working directory — the author's, untouched
├── CLAUDE.md                    # gets an appended sci-paper block naming the workspace
├── .gitignore                   # gets the build-artefact lines appended
├── data/  src/  ...             # untouched
└── paper-quenching/             # THE WORKSPACE ROOT
    ├── notes/  figures/  code/
    ├── paper/  manuscript/  .build/
```

Two things follow, and they are what keep this simple:

- **Inside the workspace root, the layout is the same in every case** (§4.2). No skill needs to know whether it is one directory down or at the top; it reads the workspace root from `CLAUDE.md` and works relative to it.
- **The workspace root may be `.`**, and is, whenever the working directory *is* the paper — nothing else in it, or a directory made for this paper alone. Forcing a wrapper subdirectory on a directory that holds only a paper is pure ceremony. `/paper-start` proposes the layout and the author decides; the default is a named subdirectory when the working directory already looks like a project (a `.git`, a `src/`, an unrelated `CLAUDE.md`, material with nothing to do with this paper) and `.` otherwise.

**The two files at the working-directory root are the whole of the system's footprint outside the workspace**, and both are additive: an appended, delimited block in `CLAUDE.md` and the missing lines in `.gitignore`. Nothing else outside the workspace root is created, moved or modified — the author's project keeps its own shape.

**`CLAUDE.md` is the load-bearing one.** It is what a new session reads automatically, so it is what names the workspace root and points at `paper/STATE.md`. A workspace that gets a `paper/` and a `manuscript/` but no `CLAUDE.md` block looks scaffolded and is not: nothing tells the next session where the memory is, and §5 quietly fails to engage.

### 4.2 Inside the workspace root

```
<workspace root>/
├── notes/                 # AUTHOR-OWNED. free-form markdown. agent writes only on request
├── figures/               # AUTHOR-OWNED
├── code/                  # AUTHOR-OWNED, optional. methods can be written from it
├── paper/                 # AGENT-OWNED MEMORY
│   ├── STATE.md               # living, ≤2 pages, rewritten each session
│   ├── journal.md             # append-only, dated
│   ├── outline.md             # the argument spine — SOLE authority for the argument
│   ├── open-questions.md      # things needing an author decision
│   └── lit/
│       ├── index.md           # one line per paper in play
│       └── <bibcode>.md       # deep notes, only for papers actually read
├── manuscript/
│   ├── main.tex               # journal class + \input of sections
│   ├── sections/*.tex
│   ├── scipaper.sty         # the gap-marker package
│   └── refs.bib               # verbatim ADS exports only
└── .build/                    # gitignored: latexmk output, rendered pages, fetched PDFs
```

Everything except `.build/` is committed. The diffs of `paper/` are the record of how the paper was thought through.

**`paper/`, `manuscript/` and `.build/` always live in the workspace root.** They are agent-owned or shared, they are created by `/paper-start`, and their location is not negotiable — that is what makes the workspace a workspace.

**The author's three directories are found, not placed.** `notes/`, `figures/` and `code/` belong to the author, so they are used wherever they already are and under whatever they are already called: `analysis/` and `plots/` in the working directory above, a `notes/` at the project root, or nothing yet at all. They are created inside the workspace root only when the material exists nowhere. Whatever the answer, the resolved paths are written into the `CLAUDE.md` block, and `% src:` anchors (§6.3) are written relative to the workspace root — so `% src: ../analysis/plot_lf.py:88 (fit_break)` is a legitimate anchor when that is where the code actually is.

Nothing the author owns is ever moved to make the layout tidier. A directory map that describes a layout the author does not have is worse than no map, and a scaffold that relocates a week of someone's work to fit a diagram is the fastest way to lose them.

---

## 5. Memory

The single most important design decision, because it is what makes a new conversation continuous with the last one.

### 5.1 Three tiers, deliberately

| File | Loaded | Lifespan | Contains |
|---|---|---|---|
| `CLAUDE.md` | automatically, every session | stable — changes rarely | **how to behave, and where things are**: the workspace root (§4.1), the sci-paper install path, directory map, venue, build command, the pointer to `STATE.md` |
| `paper/STATE.md` | first action of every session | **only true today** | **where we are**: section status, what's settled, what's open, next action, and what is currently in flux about the argument |
| `paper/journal.md` | on demand | permanent archive | **how we got here**: dated entries, what was discussed, what was decided and why |

The split test: *will this still be true in three months?* If yes it belongs in `CLAUDE.md`; if no it belongs in `STATE.md`.

**Why two tiers rather than one.** `STATE.md` is capped at two pages precisely so it can be read *in full, every time*, without thought. A single memory file either grows past the point where it is reliably read, or stays thin enough to be useless. The cap is the mechanism.

**`CLAUDE.md` holds no paper knowledge.** Knowledge placed there goes stale silently, because nothing ever prompts a review of it. Rules only.

### 5.2 STATE.md

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
- <decision> (<journal date>)   ← the date is required: it is how a later session
  finds the reasoning, and how a reversal is spotted

## Open
- <pointers into open-questions.md by id>

## Next
<the one or two things to do next>
```

### 5.3 journal.md

Append-only. One entry per working session:

```markdown
## 2026-08-21
**Discussed:** whether the bright-end cutoff needs the AGN model or follows from cooling alone.
**Decided:** keep both, present cooling first — the AGN case is stronger after the reader has seen Fig 4.
**Changed:** rewrote sections/04_results.tex §2; added 3 refs.
**Open:** need the z=2 numbers before the Discussion can close.
```

Written by whichever skill ran. Never rewritten, never pruned.

**When a decision reverses**, the new entry says so explicitly and names the date it overturns, and **every file holding current truth is brought into line** — `STATE.md`'s *Settled*, `outline.md` if the argument changed, and the question's status in `open-questions.md`. Updating only `STATE.md` would leave the sole argument authority (§4) stating the overturned position, which is worse than the problem this rule exists to solve. Nothing is edited in the journal; the correction is the newer entry. This is what stops `STATE.md` carrying a confidently-dated fact that was overturned two months ago — the failure mode a `Last updated` stamp cannot detect, because the file is fresh and the content is wrong.

### 5.4 open-questions.md

Three fields, no more — an id, a status with its date, and the question:

```markdown
- **Q7** _open_ · 2026-08-21 · Is the 100-particle cut the right one for the morphology claim?
- **Q4** _resolved 2026-08-19_ · Which cosmology to quote → WMAP1; see journal 2026-08-19
```

Ids are referenced from `\gap{q}` markers and from `STATE.md`. Resolved questions stay in the file; they are the cheapest record of why something is the way it is.

### 5.5 Literature notes

`paper/lit/index.md` is a flat roster — one line per paper: bibcode, short handle, why it is in play, and whether it has been read.

`paper/lit/<bibcode>.md` exists **only for papers actually read in depth**, and holds what it says, what we take from it, and any numbers or table rows extracted with their exact source. This asymmetry is deliberate: a stub file per search hit would be hundreds of empty files.

---

## 6. The draft is allowed to be incomplete

### 6.1 Gap markers

One LaTeX macro, five kinds:

```latex
\gap{number}{cooling threshold — need the value from run 3}
\gap{cite}{who first showed the bright-end cutoff?}
\gap{q}{is this the right sample cut? see paper/open-questions.md (Q7)}
\gap{logic}{this does not yet follow from Fig 4}
\gap{todo}{expand once the z=2 run finishes}
```

`manuscript/scipaper.sty` is small — 124 lines as built, most of it the AAS journal-abbreviation block that verbatim ADS BibTeX turned out to require (§14). Mode is a package option — `\usepackage{scipaper}` is draft, `\usepackage[final]{scipaper}` is final — so switching it is a one-word edit in `main.tex` and is visible in the diff. In `draft` mode (the default) markers render loudly inline and in the margin. In `final` mode **each `\gap` invocation** raises `\PackageError` and the build fails. The error fires on invocation, never at package load — a gap-free manuscript must build cleanly in `final` mode, or the mechanism is worthless.

Collecting the gaps is `grep -n '\\gap{' manuscript/main.tex manuscript/sections/*.tex`. Restricted to `.tex`, because `scipaper.sty` contains the macro's own definition. It does not need a tool.

**What this does and does not guarantee.** It guarantees a *marked* gap cannot reach a submitted manuscript. It does not detect a free-text `TODO`, `TBD` or `XXX`, and it cannot detect a number the agent wrote instead of marking — that is what §6.2 addresses. `/paper-finish` sweeps the free-text placeholders with one additional grep (§7.6).

This mechanism replaces the entire approval-gate apparatus of the superseded plan. The draft is not blocked from being incomplete; it is merely incapable of concealing a hole it knows about.

### 6.2 The two integrity rules

Everything else about verification is the author's. These two are kept because they are nearly free and they protect the author at the moment they are reading fast.

**Rule 1 — every quantitative statement is either traced or marked.** A number, range, threshold or uncertainty in the manuscript carries exactly one of:

- a `% src:` comment naming where it came from, or
- a `\gap{number}` marker, if it has no source yet.

There is no third option, and the agent never writes a number it cannot trace. The same applies to a citation: found and cited, or `\gap{cite}`.

**The legitimate sources are wider than the notes**, because in practice a result lives wherever the author put it:

| Source | Anchor |
|---|---|
| a note | `% src: notes/methods.md "cooling threshold"` |
| a figure the agent looked at | `% src: figures/fig3.pdf` |
| a line in the analysis code | `% src: code/plot_lf.py:88 (fit_break)` |
| a literature note | `% src: paper/lit/2020MNRAS.499.5732S.md table 2` |

**The draft is never a source.** A number cannot be justified by another sentence in the manuscript; that is circular, and it is how a transcription error propagates.

**A value read off a figure is an estimate and is labelled as one** — the author's own figures as much as published ones. An exact value must trace to a note, a table, an explicit annotation, or the code or data behind the plot. Reading a point off a plot image is approximate, and prose that quotes it to three significant figures is false precision regardless of how good the trace looks.

**Code is read, never run.** A `% src:` anchor into `code/` points at a definition or a literal in the source; it never means the agent executed anything (§3 forbids it). A result that exists only as the *output* of a run, and is not written down anywhere, has no source yet — it is a `\gap{number}` until the author records it.

**Rule 2 — BibTeX comes verbatim from the ADS export endpoint.** Never hand-written, never adjusted, never "corrected". `ads.py export` is the sole supported path to a `refs.bib` entry.

**Both rules are hard instructions, not gates.** Nothing structurally prevents an agent with write access to `refs.bib` from composing an entry, or from writing an untraced number. They make the wrong thing visible; they do not make it impossible. That is the honest description, and it is the right one — the author is the verifier, and §7.6 gives them a five-minute sweep rather than a guarantee they should not trust.

### 6.3 Source comments

The `% src:` comment is the entire traceability mechanism. There is no registry.

```latex
% src: notes/methods.md "cooling threshold"
```

Invisible in output, greppable, zero ceremony. Two rules about their form and their scope:

**Anchor by name, not by line number.** `notes/` is author-owned and edited constantly; inserting one paragraph invalidates every line pointer below it, and a link known to be stale is a link that gets ignored. Anchor on a heading or a short distinctive quoted phrase. Code is the one exception where a line number is useful, and it carries the enclosing function name alongside it.

**Comment what is load-bearing, not everything.** Every quantitative statement (required by rule 1), plus method and sample definitions and any unusually load-bearing claim. Connective and qualitative prose gets nothing — commenting every sentence buries the section diffs in comments and devalues the marks that matter.

---

## 7. Workflows

**What a session actually looks like.**

The commands below are shortcuts, **not an interface the author has to learn**. `CLAUDE.md` points every session at `STATE.md`, so opening a terminal and typing *"where were we?"* or *"the z=2 run finished, here are the numbers"* works exactly as well as a slash command. The skills exist to carry technique, not to gate access.

A normal working session, end to end:

> **`where are we?`** — reads `STATE.md`, answers in three sentences: Results is drafted with four gaps, the Discussion is stuck on the LF cutoff, Q7 is still open.
>
> **`the z=2 numbers are in run3/output.txt`** — fills two `\gap{number}` markers, traces both with `% src:`, notices that a third gap is now answerable and asks about the fourth.
>
> **`does anyone else see this turnover?`** — `/paper-lit`, novelty mode. Comes back with three papers, one of which found the opposite; that lands in `paper/lit/` and becomes an open question.
>
> **`what's still open?`** — the gap list, straight from `grep`, grouped by section. Available at any time, not only at `/paper-finish`.
>
> **[the author edits `04_results.tex` by hand for an hour]** — the next session sees those edits and works around them; it does not regenerate over them (§7.2).
>
> At the end, `STATE.md` is rewritten and a dated `journal.md` entry is appended. Tomorrow starts from there.

The measure of the design is that none of that required the author to think about the system.

Six skills. Each one reads `STATE.md` first and writes `STATE.md` + a `journal.md` entry last (§9.2).

### 7.1 `/paper-start` — ingest and orient

Reads `notes/`, **looks at** every figure (converting EPS/PS with `pdftoppm` or `gs` first), reads any tables, reads `code/` if present.

Fetches the target journal's current template and class file into `manuscript/`, and scaffolds the workspace: it proposes the workspace root (§4.1), creates `paper/` and `manuscript/` inside it, and wires the working directory by writing or **appending to** the root `CLAUDE.md` and `.gitignore`.

**The append path is the normal one, not the edge case.** An existing project already has both files, and a scaffold that merely declines to overwrite them leaves the workspace unwired: no first-action pointer, no recorded install path, and `.build/` tracked in git. The `CLAUDE.md` block is delimited by `<!-- sci-paper: begin -->` / `<!-- sci-paper: end -->` markers so it can be rewritten in place on a later run without ever touching the author's own text; `.gitignore` gets only the lines it is missing.

**The venue does not have to be decided yet.** Early on it usually is not. Absent a choice the scaffold uses a plain `article` class, and switching later is a `main.tex` preamble change plus a re-fetch — the prose does not care. Refusing to start until the author picks a journal would be exactly the wrong kind of gate.

Returns, as a conversation rather than a gate:
- a proposed **argument spine** → `paper/outline.md`
- the results as it understands them from the notes
- **what it could not work out** → `paper/open-questions.md`

It is expected to run against a thin, messy, incomplete `notes/`. Producing a short outline and a long question list is a valid and useful outcome.

### 7.2 `/paper-draft <section>` — write or rewrite a section

Draws only on `notes/`, `figures/`, `code/`, `paper/` and existing draft sections. Writes to `manuscript/sections/`.

Three drafting sources, which behave differently:

- **From notes** — the normal case. Prose follows the author's stated understanding. Anything the notes do not settle becomes a gap.
- **From code** — for Methods, when analysis code is available. Reads the source and writes what the code *does*; it never runs it (§3, §6.2). Where the code and the notes describe the method differently, that becomes a `\gap{q}` rather than a silent choice between them. This is the one place the agent is genuinely well-placed to catch something the author would miss, and it falls out of the work rather than needing machinery.
- **From figures** — the agent looks at the figure and describes what is actually plotted, then checks that against the caption and the notes.

Section *roles*, not names. This is measured, not assumed: across six of the author's own published papers, section headings are not canonical — one paper has no Results section at all, and combined "Results and Discussion" headings are common. Keying the skill to heading names would therefore fail on real papers. The skill works in terms of what a section is *doing* (methods / results / discussion / framing), and `outline.md` maps those roles onto whatever headings the paper actually uses — including a combined "Results and Discussion".

**Editing is non-destructive.** The author edits `manuscript/` directly and constantly — that is the point of the project. The agent therefore **edits in place and preserves author prose**. It never regenerates a section wholesale over existing text without showing what it would replace and being told to go ahead. A single silent overwrite of a day's hand-editing ends the author's trust in the system permanently, and git making it *recoverable* does not make it acceptable.

**The draft is not a science source.** `notes/`, `figures/`, `code/` and `paper/lit/` are where science comes from. A number or claim already in the manuscript is never evidence for another one (§6.2).

Intro, Conclusions and Abstract are directed to `/paper-frame`, which is where the technique for them lives.

### 7.3 `/paper-iterate` — the thinking loop

Where most of the author's time goes. Not "improve the prose" — a specific hunt for what is hard to see from inside one's own draft:

- a discussion point with no result behind it
- two results that quietly disagree
- a buried lead in section 4 that should be the headline
- a leap the reader will not follow
- an ordering problem — the reader needs X before Y
- a claim stated more strongly than the figure supports
- something in the notes that never made it into the draft
- a connection between two results not yet drawn

Output is a conversation plus proposed edits, never silent rewrites. Substantive exchanges land in `journal.md`.

**Where a claims-blind read is wanted** — checking whether the paper stands up to someone who has *not* been in the conversation — the skill runs that pass in a fresh subagent given the manuscript and figures but not `paper/`. This is the one place isolation genuinely buys something.

### 7.4 `/paper-lit` — the literature arm

Four modes, because they are different jobs (§8).

### 7.5 `/paper-frame` — Introduction, Conclusions, Abstract, Title

**Body first is a strong default, not a gate.** When the body is still thin, the skill says so and names what is missing — but it will still draft, and the draft comes back heavily gapped. Writing a provisional introduction is sometimes exactly how an author discovers what the paper is actually about, and refusing to do it would reintroduce "finish the science first" through the back door. A soft, self-reported section status is in any case the wrong thing to enforce a hard gate on.

The premise: once the body exists, the Introduction is largely *derivable*. The goals are in the notes, the problem and its context come from `paper/lit/`, and what the paper actually found is in the drafted Results and Discussion. Same for the Conclusions, where the value has already been fleshed out in the body.

Writes in the order: Conclusions → Introduction → Abstract → Title. Conclusions first because it forces an explicit statement of what the paper established, which the Introduction then has to motivate.

### 7.6 `/paper-finish` — close the paper

- sweep every remaining `\gap`, listed by kind and location
- sweep free-text placeholders the macro cannot catch: one grep for `TODO|TBD|XXX|FIXME|\?\?\?`
- **advisory sweep for untraced numbers** — quantitative lines carrying neither a `% src:` nor a `\gap`. This is a grep over the section `.tex` files for digit-bearing lines, minus an exclusion list (`\gap`, `\ref`, `\label`, lengths, `\section`). It is approximate and it will be noisy; it is **a list to scan, never a gate**, and it exists because checking every number is the author's stated job and this makes it a five-minute pass instead of a re-read
- fill every `\gap{cite}` via `/paper-lit`
- export the full bibliography verbatim from ADS
- compile with `latexmk`; **the `.log` is the authority** on undefined citations, undefined references and missing figure files — nothing custom needs to re-derive these
- check every float is referenced in the text, and every figure file exists
- **venue conformance, as a per-venue grep checklist** in `_shared/venues/<venue>.md` — document class and version, bibliography style, required fields, figure formats, word or page limits. Written as concrete greps against the manuscript, not as prose advice. A&A returns AASTeX-formatted or generic-article submissions **before peer review**, so this is cheap to check and expensive to miss
- build in `final` mode, which fails while any gap remains

---

## 8. The literature arm

### 8.1 Four modes

| Mode | Question | Output |
|---|---|---|
| **novelty** | "here is my result — has this been done?" | honest answer, including the bad one |
| **build-on** | "what is the closest existing work, and what did it leave open?" | ranked shortlist, with the gap each leaves |
| **support/contradict** | bound to one sentence in the draft | both directions, explicitly |
| **mine** | "pull the numbers I can compare against" | values quoted with their exact source location |

**The novelty mode has to be able to deliver bad news.** Naming a paper that scoops the result is its *successful* outcome. This is stated in the skill because it is the mode most likely to be softened by a model trying to be encouraging, and it is the mode that saves the most time.

**The mine mode** fetches the PDF where it can (§9.1) with `curl` to `.build/`, then reads it natively, and and records table rows, values and sample definitions into `paper/lit/<bibcode>.md`, each **quoted with the page or table it came from** rather than presented as a clean extraction. A mined value becomes usable in the manuscript through the ordinary `% src:` trace (§6.2). One honest limit, stated in the skill and carried into any output: **values from tables and text are reliable; reading points off a published figure is a visual estimate and must be labelled as one.** It is never quoted as a measured value.

### 8.2 Query craft

The value here is knowing how astronomers actually search, not in wrapping an API:

- `property:refereed` — the authoritative peer-review flag. Never inferred from arXiv presence.
- `database:astronomy`, `doctype:(article OR eprint)` — drops meeting abstracts, proceedings and theses, which otherwise flood results.
- `ads.py refs <bibcode>` and `ads.py cites <bibcode>` — snowballing in both directions from a seed paper. This is how prior work is actually found in astronomy, and it outperforms keyword search for the novelty and build-on modes.
- `reviews()`, `topn()`, `citation_count desc` — foundational work.
- `object:` — SIMBAD/NED-tagged source-specific literature.
- `author:` / `orcid:` — the author's own prior work, for continuity and self-citation.

Every paper that enters play gets a line in `paper/lit/index.md`. Every paper read in depth gets a note file. Literature knowledge therefore compounds across the whole project instead of evaporating each session.

---

## 9. What gets built

### 9.1 Tools: one

Every candidate tool was tested against principle 3. All but one failed:

| Candidate | Verdict |
|---|---|
| figure conversion | **Not needed.** One `pdftoppm`/`gs` invocation, documented in the skill. PNG and PDF are read natively. |
| LaTeX checking | **Not needed.** `latexmk` and the `.log` already report undefined citations and references and missing files, authoritatively. Gap collection is `grep`. |
| PDF fetching | **Not needed.** `curl` to `.build/`, then read natively. |
| repo scan / file classification | **Not needed.** glob, `ls`, Read. |
| page rendering | **Not needed.** `latexmk` then `pdftoppm`. |
| **ADS access** | **Built** — `tools/ads.py`, see below. |

**`tools/ads.py`** is the one script. Python stdlib only (`urllib`, `json`), five commands over the ADS v1 API's search and export endpoints:

| Command | Returns |
|---|---|
| `search '<solr query>'` | bibcode, title, first author, year, `refereed`, doctype, **abstract**, **DOI and arXiv id**, **`esources`** |
| `export <bibcodes...>` | **verbatim BibTeX** from the ADS export endpoint |
| `refs <bibcode>` / `cites <bibcode>` | backward and forward snowballing, same fields as `search` |
| `resolve <arxiv-id\|doi>` | → bibcode, **preferring the refereed record** where a preprint has a published version |

The bolded fields are not optional extras: without the abstract, the novelty and support/contradict modes cannot screen anything; without the identifiers, the mine mode cannot find a PDF to read and §10 cannot fetch arXiv source. A command set that returns less than this looks smaller but makes §8 unbuildable.

**`esources` returns source *types* (`eprint_pdf`, `pub_html`, …), not URLs**, so retrieval is a short ladder rather than a field lookup: an arXiv id gives `arxiv.org/pdf/<id>` directly, which covers nearly everything in astronomy; otherwise the ADS link gateway is constructible as `https://ui.adsabs.harvard.edu/link_gateway/<bibcode>/<TYPE>`; and where neither resolves, the mine mode **says the paper could not be fetched automatically and gives the author the link**, rather than silently returning nothing.

**Redirects are rejected**, or at minimum every cross-origin redirect is, and the target is reported without the token. `urllib` follows redirects by default and can carry an `Authorization` header to a host that was never intended to see it. This is a few lines and it is the one security-relevant behaviour in the project.

Token resolution, in order, so it works on a laptop and on OzSTAR/NERSC alike: macOS Keychain → `ADS_API_TOKEN` → `ADS_DEV_KEY` → `SCIX_API_TOKEN` → `~/.ads/dev_key`. Never in a URL, never on argv, never logged. Base URL from `SCI_PAPER_ADS_BASE`, defaulting to `https://api.adsabs.harvard.edu/v1`; SciX is a one-variable switch, as both hosts serve the same v1 Solr surface. Every command whose input is a *query* takes an explicit row limit with a bounded default, so a broad query neither truncates silently nor pulls an unbounded result set. `export` is exempt and deliberately so: it takes an explicit list of bibcodes, so its input already is its bound.

396 lines as built. The estimate at design time was 200; the difference is almost entirely the token-safety work in §14, which was not foreseen and was worth every line of it. It exists because the alternatives are worse: the API needs a bearer token in a header, it paginates, and `export` is what keeps rule 2 honest.

**Deliberately not an MCP server.** The official `adsabs/scix-mcp` covers this ground, but it brings node, `npx` and MCP client configuration for what is a few hundred lines of stdlib Python, and it puts the verbatim-BibTeX guarantee in someone else's repository. A script the skills invoke is simpler to install, simpler to test, and version-pinned by being in this repo.

**So the code in this project is `tools/ads.py` and `scipaper.sty` — a few hundred lines in total.** Everything else that gets built is skill content and the memory convention.

The consequence, which should be stated plainly: **the entire value of this project lies in how specific the skill files are.** Vague skill prose will produce generic output, and no amount of Python fixes that. Effort goes into the actual query patterns, the actual iteration checklist, the actual rhetorical moves — not into infrastructure.

### 9.2 Skills, and the DRY rule that binds them

`built` marks what exists today; the rest is the remaining phases (§11).

```
tools/ads.py             # the only script                              built
skeleton/                # copied into a paper repo by /paper-start     built
skills/
├── _shared/
│   ├── memory.md        # read STATE.md first; write STATE.md + journal.md last
│   ├── house-rules.md   # the two integrity rules, source comments, gap markers,
│   │                    #   non-destructive editing, locating the installation
│   ├── sections/*.md    # rhetorical moves per section role — data, not skills
│   │                    #   methods, results, discussion built; framing is P5
│   └── venues/*.md      # per-venue conformance checklists, as greps    P5
├── paper-start/SKILL.md                                              # built
├── paper-draft/SKILL.md                                              # built
├── paper-lit/SKILL.md                                                # built
├── paper-iterate/SKILL.md                                            # P4
├── paper-frame/SKILL.md                                              # P5
└── paper-finish/SKILL.md                                             # P5
```

**`_shared/sections/` holds only roles that exist.** A role file that is named by
`outline.md` but absent sends the drafting skill looking for a file that is not
there — `framing` was written into an outline before `/paper-frame` existed and
did exactly that. Do not name a role before its file is written.

The memory protocol and the house rules are written **once** in `_shared/` and referenced by every skill. Restating them six times is how they drift.

Per-section rhetorical moves are **data in `_shared/sections/`**, not one skill per section: the procedure for drafting a section is identical, only the moves differ.

### 9.3 External dependencies

| Dependency | Purpose | Already present |
|---|---|---|
| Python 3.11+ (stdlib only) | `tools/ads.py` | yes — 3.14.6 |
| an ADS/SciX API token | all literature access | one-time, free |
| `latexmk` / `pdflatex` | build | yes |
| `pdftoppm`, `gs` | figure and page rasterisation | yes |
| `curl`, `git`, `grep` | — | yes |

No third-party Python packages, no virtualenv, no node, no MCP client. Nothing to install but a token.

---

## 10. Style and venue

**The container** — class file, required fields, section requirements, figure formats, submission rules — comes from the **journal's current template, fetched at `/paper-start`**. Journal classes drift independently and continuously (AASTeX 7.0.1, `mnras.cls` 3.3, `aa.cls` 9.4, one of which changed within six months), so fetching beats anything written into a skill.

**The rhetoric** — how a results paragraph is built, how a discussion moves from result to interpretation to caveat — comes from `_shared/sections/*.md`. These are written once, by hand, and are the highest-value content in the project (§9.1).

**Optional, on request only:** the author can name recent papers they think are well written and `/paper-draft` will fetch the LaTeX source from arXiv (`arxiv.org/e-print/<id>`) as a style reference for that session. No phase owns this and nothing fetches it automatically — it is a thing the author asks for when the prose is not sounding right, not a pipeline step.

**The author's own voice** is an **opt-in** style reference, not a default. It is often wrong for a multi-author paper, and a style-matching pass that always runs is an irritation.

The author's 2004–2016 corpus is **retired** as a foundation. It was load-bearing for the superseded plan because that plan parsed existing manuscripts; here the system writes the manuscript and controls the constructs. Nothing from it ships in this repo: where the author wants an old paper as context they point the agent at it on disk, which is the ordinary opt-in style-reference path above.

---

## 11. Build order

Each phase leaves the system usable. Nothing is built ahead of a demonstrated need.

| Phase | Deliverable | Done when | Status |
|---|---|---|---|
| **P1** | Workspace skeleton, `CLAUDE.md` template, `scipaper.sty`, `_shared/memory.md` + `house-rules.md` | scaffolding a repo by hand produces a draft-mode build that fails in `final` mode with one gap present | **done**, verified 2026-08-21 (§14.1) |
| **P2** | `/paper-start` + `/paper-draft` | **the minimum useful system.** A real `notes/` + `figures/` directory produces a compiling, honestly-incomplete body draft | **done**, verified 2026-08-21 (§14.2) |
| **P3** | `tools/ads.py` + `/paper-lit` + `paper/lit/` convention | all four modes run; BibTeX arrives verbatim from `export`; a novelty check returns a real prior-work answer, including an unwelcome one | **done**, verified 2026-08-22 (§14.3) |
| **P4** | `/paper-iterate` | a session produces substantive structural criticism, not copy-editing, and lands in `journal.md`. **Prototype this one against a real draft before writing the final skill file** — it carries the most value and the most risk, and it is the only skill whose quality cannot be judged by reading it | **next** |
| **P5** | `/paper-frame` + `/paper-finish` | Intro and Conclusions written from a completed body; `final` build succeeds with zero gaps | not started |
| **P6** | Dogfood on a real paper end to end | the author would use it again | not started |

**After P2 the system already earns its place.** P3–P5 deepen it. If P4 or P5 turn out not to be worth the skill file, they should not be written.

### 11.1 How the remaining work batches

Which phases can share a session, and which must not. This is about what can be
*demonstrated* together, not about size.

**P4 — alone, and it is really two sittings.** The prototype-before-writing
instruction above is a requirement, not a suggestion, because `/paper-iterate`
is the only skill whose quality cannot be judged by reading it. So: one sitting
that runs the §7.3 moves by hand against an actual draft and keeps only what
produced substantive structural criticism, then a second that writes the skill
file from what survived. Nothing else shares either sitting — the failure mode
is degenerating into copy-editing, and that is invisible if the session is also
busy with something else. It also wants a draft thicker than the two-section
acceptance fixture, so it is better run against a real paper. This is the one
skill that uses subagent isolation (the claims-blind read, §7.3).

**P5 — one session, both skills.** `/paper-frame` and `/paper-finish` share a
single acceptance criterion: Introduction and Conclusions written from a
completed body, then a `final` build that succeeds with zero gaps. The second is
not demonstrable without the first, so splitting them buys nothing. Note that
`/paper-finish` needs `_shared/venues/<venue>.md`, which needs a venue actually
chosen — if none is, write the skill against one real venue rather than
inventing a generic checklist.

**P6 — alone, and it is not a coding session.** Dogfooding a real paper end to
end runs over weeks of ordinary use, and its output is a list of fixes to
everything built before it. Nothing is scheduled alongside it.

**Nothing else combines.** The phases are already the smallest units that leave
the system usable.

---

## 12. Deliberately not in v1

Named so that scope creep is visible when it is proposed:

- No approval registry, claims database, results database, or state validator.
- No numeric consistency checking, unit algebra, or $h$-scaling verification.
- No provenance graph binding figures to scripts to columns.
- No style policing, banned-word lists, or AI-writing detection.
- No figure generation, re-plotting, or re-running of analysis.
- No co-author merge or comment-resolution workflow.
- No response-to-referee workflow. *(The strongest v2 candidate — the memory in `paper/` is exactly what a referee response needs, and it is the same machinery pointed at a different document.)*
- No submission-portal automation.

---

## 13. Risks

1. **Skill files that are vague produce generic prose.** The whole project rests on their specificity. Mitigation: P6 dogfooding on a real paper is the only real test, and it is a phase, not an afterthought.

   The two adoption killers this design exists to avoid are not technical: **a draft that marks the author's own known results as gaps** because they live in a figure rather than a note (§6.2 makes figures and code first-class sources), and **an agent that overwrites hand edits** (§7.2 forbids it). The third has no design fix: if `/paper-iterate` returns advice indistinguishable from a generic "review my draft" prompt, editing directly is simply faster. That one is won or lost in the skill file, and it is the thing to watch in P4.
2. **The memory decays if sessions end without writing it.** A skill that fails to update `STATE.md` breaks continuity silently. Mitigation: it is the *last* instruction in `_shared/memory.md`, and `STATE.md` carries a visible `Last updated` date the author will notice going stale.
3. **`STATE.md` grows past being read.** The two-page cap is the mechanism, and it must be enforced by rewriting rather than appending.
4. **`/paper-iterate` degenerates into copy-editing**, which is the failure mode of every "review my draft" prompt. Mitigation: the checklist in §7.3 is specific and structural, and copy-editing is explicitly out of scope for that skill.
5. **The novelty mode softens bad news.** Mitigation: stated as the success condition in the skill.
6. **Figure-derived values leak into the paper as if measured.** Mitigation: the visual-estimate rule in §6.2, which covers the author's own figures as well as published ones.
7. **`tools/ads.py` is the one piece of code that can break.** It is small, stdlib-only, and depends on a stable public API, so the exposure is low — and unlike a silent wrong answer, an API failure is loud and immediate. A redundant second client is not insurance worth its weight: the real fallback is `curl` against the same documented endpoint for a session, or the ADS website. Both `api.adsabs.harvard.edu` and `api.scixplorer.org` serve the same v1 surface, so a host outage is one environment variable.
8. **Writing before the results are settled means text that has to change.** This is accepted and is the point of the project. `\gap{number}` and the `% src:` comments are what make the eventual sweep tractable.

---

## 14. Validation record

What has actually been built, and what was verified rather than asserted. Every
claim here was produced by running something, not by reading it.

The acceptance fixture is `.dogfood/quenching/` — local only, untracked, and
**kept deliberately**. It is a purpose-built messy paper directory: three
free-form notes, five figures (one EPS-only, one orphaned, one misleading `_old`
sibling that is a *different* plot), two analysis scripts carrying twelve
planted inconsistencies, and now P3's literature output on top. It is the
cheapest regression test for any later change to `/paper-start`, `/paper-draft`
or `/paper-lit`; `.figsrc/PLANTED.md` lists what each defect was planted to
catch.

### 14.1 P1 — the gap mechanism

Three properties, each re-verified after every subsequent change to the package:

- draft mode builds — exit 0;
- `[final]` mode with gaps present fails — exit 12, one `Package scipaper
  Error` per `\gap` invocation;
- `[final]` mode with **zero** gaps builds cleanly — exit 0. This is the
  property that makes the mechanism worth anything, and it is the one an
  error-at-package-load implementation would break.

Verified with gaps in section text, `\title`, a heading, math mode, a
`\caption`, a float, a `minipage`, a footnote, a `tabular`, the table of
contents and the list of figures.

**Two build-breaking defects in the package were found by using it, not by
reading it.**

1. `\gap` originally used `\marginpar`, which goes through LaTeX's float
   mechanism: inside a `minipage` or a footnote it raises "Not in outer par
   mode" or loses the float, and the build fails. Both are ordinary places for
   a gap in an astronomy manuscript. It now uses `marginnote`, which places the
   note directly. `\gap` is also declared with `\DeclareRobustCommand`, so a gap
   in a caption or a heading survives into the `.aux` as itself.
2. Verbatim ADS BibTeX writes journal names as AAS macros (`\apj`, `\mnras`),
   which a plain `article` class does not define — so the *first* exported
   reference broke the build with `Undefined control sequence`. That made rule 2
   (§6.2) unusable for exactly as long as the venue is undecided, which is
   deliberately most of a project's life. `scipaper.sty` now provides the
   abbreviations via `\providecommand` inside `\AtBeginDocument`, so a real
   journal class always wins.

### 14.2 P2 — the minimum useful system

`/paper-start` then `/paper-draft` run against the fixture produced a workspace,
an outline, seventeen open questions, and two body sections that **build clean
from cold — exit 0, zero LaTeX warnings** — carrying 19 `\gap` markers and 29
`% src:` traces. **All twelve planted defects were surfaced as questions or gaps
rather than smoothed over**, and four further problems emerged that were never
planted, the sharpest being that the paper's stated point rests on nothing in
the material.

**Four defects in the skill files were found by running them:** `pdftoppm`
needed `-singlefile` (it was writing `fig3-1.png`, so the read failed); `gs`
needed `-dEPSCrop` (it rendered a near-blank US-Letter page instead of the
figure); the scaffold copy needed `cp -Rn`, because a plain `cp -R` silently
clobbers an author-edited `CLAUDE.md`; and the documented `latexmk` line needed
`-interaction=nonstopmode` — **without it the build hangs at LaTeX's `?`
prompt**, which in `final` mode is the normal path rather than an unlucky one.

**The single most instructive finding of the whole build** came from external
review of this phase: the acceptance draft contained a **reversed scientific
claim carrying a valid-looking `% src:` trace** — it said the model fell *below*
the observed stellar mass function at the massive end where the plotted data
have it *above* by ~0.2 dex. Verifying that surfaced something the reviewer had
not: every code line anchor in the draft was off by two, and one named the wrong
function, because they were written from memory of the file rather than from the
file. This is precisely the failure the project exists to prevent, and it
reached a draft *with a trace attached*.

The systemic fix is **step 5 of `/paper-draft`, "read every trace back before
you build"**: re-open every cited source, check the direction of every
comparison, check the named symbol owns the line, sweep for untraced captions.
It is the most important single addition to any skill file, and it is why §6.3's
traces are only worth something when something re-reads them.

**Two caveats, stated because they matter.**

The fixture was written by the same session that then drafted against it. It
tests the procedure and the toolchain honestly, but it is a weak test of whether
the skill prose guides a *cold* reader. That is what P6 is for.

And the fixture is a **root-layout** workspace: the working directory *is* the
paper. The workspace-root design of §4.1 — a named subdirectory inside an
existing project, with `CLAUDE.md` and `.gitignore` appended rather than created
— was specified after P2 was validated and **has not been dogfooded**. The
root-layout path it replaces is unchanged and still covered by the fixture, but
the subdirectory path, the append-to-existing-`CLAUDE.md` block and the
`../analysis/`-style author paths are so far only specified. First real use of
`/paper-start` in a project directory is the test, and it should be treated as
one.

### 14.3 P3 — the literature arm

**The acceptance criterion, met and re-run at the end:** all four modes ran
against the live API; eight `refs.bib` entries **byte-identical** to a fresh
single-call `export`; the novelty check returned bad news on *both* halves of
the fixture paper's claim.

**The novelty result is the part worth reading, because it is the mode working
as designed.** The fixture paper claims satellites quench above a host halo mass
of $10^{12.5}$ and that the transition barely moves to $z=1$. The literature was
not kind to either half. Peng+12 tests halo mass against local over-density *by
name* and finds over-density wins — so the x-axis of the paper's main figure may
be the wrong variable, and the *orphaned* figure, which plots exactly that, may
be the real main figure. Wetzel+12 measures no minimum halo mass at all, so
"transition" may be the wrong word. Wetzel+13 attributes the halo-mass trend to
group preprocessing. And on redshift the honest answer turned out sharper than
the first one: nothing measures the evolution of the *halo-mass* crossing point,
so the claim is **untested rather than contested** — a better position for the
paper and a worse one for its evidence.

**Token safety — four real defects, each found by a separate review round and
each verified by reproduction before being fixed.** This is the project's one
security-relevant behaviour and it is the reason the review rounds paid for
themselves:

1. The token reached stderr whenever the far end echoed the `Authorization`
   header — in an error body, a reason phrase, or a redirect `Location`.
   Reproduced against a local server; fixed by scrubbing every server-controlled
   string.
2. The body was **truncated to 400 bytes before scrubbing**, so a token
   straddling the boundary left a cleartext prefix. Scrub now runs first.
3. `build_opener` keeps urllib's environment proxy handler, so `http_proxy` plus
   a plain-HTTP base would hand the header to an unconfigured proxy. The
   proposed fix — disable proxies — was **rejected** (§15); instead the base
   must now be `https`, loopback excepted, which closes cleartext transmission
   generally rather than one instance of it.
4. The loopback exception was still proxy-bypassable. Fixed by disabling proxies
   *only* for loopback, which is correct behaviour regardless of the token.

The invariant that came out of it: **the token travels either over TLS to a
remote host, or unproxied to loopback, and nowhere else.** The TLS guard admits
`https` and loopback and refuses fourteen probed bypass forms, including the
userinfo spoof.

**Also fixed in `ads.py`:** a `TypeError` in `resolve`'s sort key when a record
has no `year`; a silently-empty result when a DOI or arXiv id is pasted as a URL
or carries a `.pdf` or `vN` suffix; a traceback rather than a message on a
stalled read or a non-JSON body; an empty-but-set `SCI_PAPER_ADS_BASE`
building a host-less URL; and `export`'s missing-bibcode check using a substring
match, so one bibcode being a prefix of another hid a dropped reference.

**In the skill prose**, three changes matter more than the rest. The PDF fetch
ladder claimed `curl -f` prevents saving a paywall page; it does not, since a
cookie wall answers 200 with HTML — the ladder now restricts itself to PDF
source types and checks for `%PDF`. Support/contradict gained a
**comparability check** — same dependent quantity, same independent variable,
comparable sample and epoch, with **adjacent** as the honest verdict when they
do not line up; this came from catching two papers being called *contradictions*
when they measure an efficiency against local density, and it is the single most
valuable change of the phase. And a hard-coded `year:2023-2026` would have gone
stale inside a project measured in months.

**Three defects were found by re-reading rather than by review**, which is worth
knowing about the limits of a review panel: a literature note read a figure
across two *different* stellar-mass curves; two scratch `.tex` files left in the
fixture by a build test were never deleted because `rm -f` is refused in this
sandbox and the exit code went unchecked, inflating the reported gap count; and
a documented `grep -q '<bibcode>'` left the bibcode's dots as regex wildcards.

**Final P3 state, all re-verified after the last fix:** five `ads.py` commands
run live; `refs.bib` byte-identical to a fresh export; the fixture builds from
cold at exit 0 with **zero LaTeX warnings, zero undefined citations, 21 `\gap`
markers, 30 `% src:` traces, 22 open questions**; `[final]` fails as designed
and a gap-free `[final]` with real citations exits 0; every `_shared/` reference
resolves.

### 14.4 How the review was run, and what it was worth

P1–P3 were reviewed by an external two-harness panel: **codex CLI / gpt-5.6-sol**
and **opencode CLI / opencode-go/hy3**, both read-only, both high effort,
staggered starts, each round a cold session re-deriving its own findings rather
than grading the previous round. Every finding was independently verified before
being accepted. P2 took three rounds; P3 took seven. The final round of each:
both harnesses `RESULT: pass`, no blocking findings.

Two honest observations about the method, since it is expensive:

- **The value was concentrated.** For P3 it was almost entirely the four token
  defects. For P2 it was the reversed claim and a build-and-report block that
  grepped the wrong directory (`cd manuscript && latexmk` followed by `grep -rn
  ... manuscript`, which searches `manuscript/manuscript`, finds nothing, and
  would report a clean draft with every gap still in it). Everything else was
  narrower instances of findings already closed.
- **Where the two harnesses disagreed, they were at the noise floor.** Their
  disagreements were about threat model and about how much role-specific
  restatement counts as DRY duplication — not about fact. Two competent
  reviewers landing on opposite verdicts is the signal to stop, not to run
  another round.

A developer's own fresh-eyes pass after the panel still found four things the
panel had not, all of them in the prose rather than the code: an outline role
pointing at a `_shared/sections/` file that does not exist, an ambiguous
back-reference that read as the skill's own §3 rather than the paper's, a stale
count of drafting sources, and two passages mangled into run-on prose by
successive edits. For a product whose entire value is the clarity of its prose,
that last one is a real defect and not a cosmetic one.

---

## 15. Settled decisions

Recorded so they are not re-opened without new evidence. Each of these was
argued at least once and in several cases repeatedly.

**The design**

- **The author is the sole verifier.** The system never certifies a number,
  method or citation. It makes work visible and traceable, nothing more.
- **Zero verification machinery.** No approval registries, claims or results
  databases, state validators, provenance graphs, numeric checkers, unit or
  $h$-scaling algebra, terminology checks, or style policing. The superseded
  design was built around these; §12 is the list and §1 the reason.
- **Both integrity rules are hard instructions, not gates** (§6.2). Do not
  describe them as structurally guaranteed. Nothing prevents an agent with write
  access from composing a BibTeX entry or writing an untraced number.
- **One shared traceability rule, and notes are not its only legitimate source**
  (§6.2). An earlier draft made notes the only source, and it was the single
  worst defect found in review: it would have marked the author's own
  figure-derived results as unknown.
- **Slash commands are shortcuts, not an interface** (§7). Plain conversation
  must work identically; `CLAUDE.md` points every session at `paper/STATE.md`.
- **KISS and DRY are binding, not preferences.** Rules live in exactly one place
  (`skills/_shared/`), referenced by the skills, never restated. Every canonical
  phrase must grep-resolve to exactly one file.
- **No MCP servers.** ADS access is `tools/ads.py`, stdlib only (§9.1). This was
  an explicit author instruction, not an inference from §9.1's reasoning.

**The token, whose threat model was settled over four rounds**

- The invariant is in §14.3. **Deliberately out of scope: a configured host
  echoing the token back** in a *successful* body — base64- or
  percent-encoded, or split across the reason phrase and the body. That host
  already holds the cleartext and the echo reaches only the operator's own
  terminal, so the defence buys nothing — and the content filter it would need
  must sit in front of the verbatim-BibTeX guarantee that rule 2 depends on.
  `_scrub`'s docstring states this limit rather than overclaiming it. One
  harness re-raised this every round; it was rejected every round, and the other
  harness agreed each time.
- **Proxies stay enabled for remote hosts.** Disabling them was proposed and
  rejected: on OzSTAR or NERSC a proxy is how you reach the internet at all, and
  over HTTPS it sees only a `CONNECT` tunnel. They are disabled for loopback
  only, where urllib would otherwise route `127.0.0.1` through `http_proxy`.

**Approaches already declined**

- **An `implementation-plan` / `scoped-implementation` / `drift-audit` workflow
  for this build.** Greenfield, no regression surface, and §11 already provides
  phased acceptance criteria. The deliverable is mostly prose, which frozen
  slices cannot audit.
- **A second, redundant ADS client** as insurance against `ads.py` breaking.
  Complexity before need; the real fallback is `curl` against the same
  documented endpoint (§13, risk 7).
- **One skill per manuscript section.** The drafting procedure is identical;
  only the rhetorical moves differ, and those are data in `_shared/sections/`
  (§9.2).
- **Building the author's paper corpus into the system as a foundation** (§10).
- **Scanning *successful* ADS responses for the token** before parsing or
  printing them. See the threat model above.
- **Citekey rekeying to `LastName_Year`.** Rule 2 says nothing is adjusted, so
  the citekey stays whatever bibcode ADS exports.

---

## 16. Installation

The system is installed **once, globally**, and each paper gets a workspace
scaffolded by `/paper-start` (§4) wherever the author is working. Nothing about a
paper lives in this repo, and the only thing about the system that lives in a
paper's directory is the recorded install path (§4.1).

### 16.1 Where it lives

This repo is composed into the shared agent home (`~/.agents`, see that repo's
`README.md`) as a manifest-managed clone under `repos/sci-paper`. Setup links
every directory in `skills/` that contains a `SKILL.md` into the single public
catalogue `~/.agents/skills/`, which each harness points at in turn. So
`/paper-start`, `/paper-draft` and `/paper-lit` are available from **any**
working directory, without that directory knowing anything about this repo.

`skills/_shared/` has no `SKILL.md` and is therefore *not* linked as a skill,
which is correct: it is data the skills read, not a skill. It stays reachable
because path resolution follows the symlink — `<skill>/../_shared/` resolves
into this repo's real `skills/` directory.

### 16.2 Locating the installation from inside a skill

`skeleton/` and `tools/ads.py` sit one level *above* `skills/`, so a skill
reaching them cannot use a path relative to the catalogue. The resolution rule
is canonical in `_shared/house-rules.md` and is stated once there:

> the installation root is two levels above the directory holding the running
> `SKILL.md`, resolved **physically** through the symlink — and it is confirmed
> by the presence of `tools/ads.py`.

**"Physically" is the whole of it.** A shell's `cd` resolves `..` against the
path as typed rather than against where the symlink points, so the obvious
`cd <skill dir>/../..` lands two levels above the *catalogue* and not above the
real `skills/`. It was written that way first and it returns a directory that
exists and holds no `tools/`, which is why the `ads.py` check is a confirmation
rather than a formality: the failure mode is a plausible wrong answer, not an
error. `cd -P` is required.

This matters at exactly one moment and it is easy to miss: **the first
`/paper-start` in a brand-new working directory.** Every later session finds the
absolute path recorded in the `CLAUDE.md` block, which the scaffold writes. The
first one has no block to read, so it must resolve the root itself or it cannot
copy the skeleton at all.

### 16.3 The ADS token

Resolution order is in §9.1. On this machine the token is in the macOS Keychain
under service `nasa-ads-api-token`, which is first in that order, so nothing
needs to be set per shell:

```sh
security add-generic-password -a "$USER" -s nasa-ads-api-token -w <token> -U
```

**The current token was pasted into a chat transcript when it was supplied.**
Rotate it at `scixplorer.org` whenever convenient; re-storing it is the one
command above and nothing else changes.

### 16.4 Working on the system while using it

The catalogue clone under `repos/sci-paper` is managed by setup, which pulls
it. Development happens in the primary clone, not in the managed one: **edit,
commit, push, then re-run `setup.sh`** to bring the global installation forward.
Editing the managed clone directly means the next `setup.sh` pull either
conflicts or quietly reverts the work.
