# astro-paper — Plan

**Version:** 1.0
**Date:** 2026-08-21
**Author:** Darren Croton (Swinburne), with Claude Opus 5
**Status:** ready to build

> **Relationship to earlier work.** This supersedes an earlier design that solved a different problem: mechanically verifying a finished manuscript's integrity via approval registries, gates and deterministic checkers. On author direction that project is abandoned. The author is the verifier and reads the paper in detail, repeatedly. What is needed instead is a **writing collaborator with durable memory and a strong literature arm**. Two supporting documents survive and remain valid: `astro-paper - Corpus Evidence.md` and `astro-paper - Ecosystem Research Record.md`.

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

The system is installed once. Each paper gets a workspace scaffolded into its own repository by `/paper-start`.

```
<paper repo>/
├── CLAUDE.md              # scaffolded: house rules + pointer to STATE.md
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
│   ├── astropaper.sty         # the gap-marker package
│   └── refs.bib               # verbatim ADS exports only
└── .build/                    # gitignored: latexmk output, rendered pages, fetched PDFs
```

Everything except `.build/` is committed. The diffs of `paper/` are the record of how the paper was thought through.

---

## 5. Memory

The single most important design decision, because it is what makes a new conversation continuous with the last one.

### 5.1 Three tiers, deliberately

| File | Loaded | Lifespan | Contains |
|---|---|---|---|
| `CLAUDE.md` | automatically, every session | stable — changes rarely | **how to behave**: house rules, directory map, venue, build command, the pointer to `STATE.md` |
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

`manuscript/astropaper.sty` is roughly 25 lines. Mode is a package option — `\usepackage{astropaper}` is draft, `\usepackage[final]{astropaper}` is final — so switching it is a one-word edit in `main.tex` and is visible in the diff. In `draft` mode (the default) markers render loudly inline and in the margin. In `final` mode **each `\gap` invocation** raises `\PackageError` and the build fails. The error fires on invocation, never at package load — a gap-free manuscript must build cleanly in `final` mode, or the mechanism is worthless.

Collecting the gaps is `grep -n '\\gap{' manuscript/main.tex manuscript/sections/*.tex`. Restricted to `.tex`, because `astropaper.sty` contains the macro's own definition. It does not need a tool.

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

Fetches the target journal's current template and class file into `manuscript/`, and scaffolds `CLAUDE.md`, `paper/`, `main.tex` and `astropaper.sty`.

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

Section *roles*, not names: the corpus evidence shows no astronomy paper reliably uses canonical headings, and one has no Results section at all. The skill works in terms of what a section is *doing* (methods / results / discussion / framing), and `outline.md` maps those roles onto whatever headings the paper actually uses — including a combined "Results and Discussion".

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

Token resolution, in order, so it works on a laptop and on OzSTAR/NERSC alike: macOS Keychain → `ADS_API_TOKEN` → `ADS_DEV_KEY` → `SCIX_API_TOKEN` → `~/.ads/dev_key`. Never in a URL, never on argv, never logged. Base URL from `ASTRO_PAPER_ADS_BASE`, defaulting to `https://api.adsabs.harvard.edu/v1`; SciX is a one-variable switch, as both hosts serve the same v1 Solr surface. Every command takes an explicit row limit with a bounded default, so a broad query neither truncates silently nor pulls an unbounded result set.

Roughly 200 lines — an estimate, not a cap. It exists because the alternatives are worse: the API needs a bearer token in a header, it paginates, and `export` is what keeps rule 2 honest.

**Deliberately not an MCP server.** The official `adsabs/scix-mcp` covers this ground, but it brings node, `npx` and MCP client configuration for what is a few hundred lines of stdlib Python, and it puts the verbatim-BibTeX guarantee in someone else's repository. A script the skills invoke is simpler to install, simpler to test, and version-pinned by being in this repo.

**So the code in this project is `tools/ads.py` and `astropaper.sty` — a few hundred lines in total.** Everything else that gets built is skill content and the memory convention.

The consequence, which should be stated plainly: **the entire value of this project lies in how specific the skill files are.** Vague skill prose will produce generic output, and no amount of Python fixes that. Effort goes into the actual query patterns, the actual iteration checklist, the actual rhetorical moves — not into infrastructure.

### 9.2 Skills, and the DRY rule that binds them

```
tools/ads.py             # the only script
skills/
├── _shared/
│   ├── memory.md        # read STATE.md first; write STATE.md + journal.md last
│   ├── house-rules.md   # the two integrity rules, source comments, gap markers,
│   │                    #   non-destructive editing
│   ├── sections/*.md    # rhetorical moves per section role — data, not skills
│   └── venues/*.md      # per-venue conformance checklists, as greps
├── paper-start/SKILL.md
├── paper-draft/SKILL.md
├── paper-iterate/SKILL.md
├── paper-lit/SKILL.md
├── paper-frame/SKILL.md
└── paper-finish/SKILL.md
```

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

The author's 2004–2016 corpus is **retired** as a foundation. It was load-bearing for the superseded plan because that plan parsed existing manuscripts; here the system writes the manuscript and controls the constructs. Two or three trimmed `.tex` excerpts are kept for the minor path where the author points the agent at an old paper for context.

---

## 11. Build order

Each phase leaves the system usable. Nothing is built ahead of a demonstrated need.

| Phase | Deliverable | Done when |
|---|---|---|
| **P1** | Workspace skeleton, `CLAUDE.md` template, `astropaper.sty`, `_shared/memory.md` + `house-rules.md` | scaffolding a repo by hand produces a draft-mode build that fails in `final` mode with one gap present |
| **P2** | `/paper-start` + `/paper-draft` | **the minimum useful system.** A real `notes/` + `figures/` directory produces a compiling, honestly-incomplete body draft |
| **P3** | `tools/ads.py` + `/paper-lit` + `paper/lit/` convention | all four modes run; BibTeX arrives verbatim from `export`; a novelty check returns a real prior-work answer, including an unwelcome one |
| **P4** | `/paper-iterate` | a session produces substantive structural criticism, not copy-editing, and lands in `journal.md`. **Prototype this one against a real draft before writing the final skill file** — it carries the most value and the most risk, and it is the only skill whose quality cannot be judged by reading it |
| **P5** | `/paper-frame` + `/paper-finish` | Intro and Conclusions written from a completed body; `final` build succeeds with zero gaps |
| **P6** | Dogfood on a real paper end to end | the author would use it again |

**After P2 the system already earns its place.** P3–P5 deepen it. If P4 or P5 turn out not to be worth the skill file, they should not be written.

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
