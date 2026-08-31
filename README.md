# sci-paper

**Work in progress — build under way.**

A small set of [Claude Code](https://claude.com/claude-code) skills that help a working astronomer turn notes, figures, tables and analysis code into a journal paper — and then keep working on it for as long as it takes.

It is built for the way papers actually get written: **starting before the picture is complete, and letting the writing shape the result.** The first draft it produces is deliberately incomplete, with every hole marked rather than smoothed over. From there it iterates with you — suggesting connections, hunting the literature for supporting and contradicting work, filling references — and writes the Introduction and Conclusions last, once there is something to introduce and conclude.

The astronomer is the verifier. The system never claims a number, method or citation is correct; it makes what it did visible and traceable so you can check it fast.

## Status

| | |
|---|---|
| Design | complete — see [`docs/sci-paper - Plan.md`](docs/sci-paper%20-%20Plan.md), which is also the build record |
| Implementation | **P3 done, retrofitted onto an isolated-workspace layout (P3.5).** `/paper-start` and `/paper-draft` take a real `notes/` + `figures/` + `code/` directory to a compiling, honestly-incomplete body draft, scaffolded into its own git-isolated `sci-paper-workspace/`; `tools/ads.py` and `/paper-lit` add the literature arm; `/paper-voice` distils past papers into a per-paper style profile. P4 (`/paper-iterate`) next |

## What is here

```text
docs/sci-paper - Plan.md   # the design, the build record and the status. start here
tools/ads.py                 # the only script: ADS/SciX, stdlib only
skills/
├── _shared/
│   ├── memory.md            # what to read first, what to write last, paper/lit/
│   ├── house-rules.md       # integrity rules, gap markers, % src:, the workspace root
│   └── sections/            # rhetorical moves per section role — data, not skills
├── paper-start/SKILL.md     # ingest, look at the figures, propose the argument
├── paper-voice/SKILL.md     # distil past papers into this paper's own voice profile
├── paper-draft/SKILL.md     # write one section; mark what it cannot answer
└── paper-lit/SKILL.md       # query craft and the four literature modes
skeleton/
├── root/                    # appended into the working directory (an index only)
└── workspace/                # copied to become sci-paper-workspace*/
    ├── CLAUDE.md
    ├── paper-voice/README.md
    ├── paper/                 # STATE, journal, outline, open questions, lit
    └── manuscript/            # main.tex + scipaper.sty
```

## Shape of it

Seven skills, one 396-line stdlib script for ADS access, and a 124-line LaTeX package — the gap-marker macro plus the AAS journal abbreviations that verbatim ADS BibTeX needs. No MCP servers, no databases, no schemas. Almost all the value is in how specific the skill files are, not in the code.

- `/paper-start` — read the notes, look at the figures, propose an argument and a list of questions
- `/paper-voice` — distil past papers or style notes into this paper's own voice profile
- `/paper-draft` — write a section from notes, code or figures; mark what it cannot answer
- `/paper-iterate` — the thinking loop: connections, tensions, buried leads, ordering
- `/paper-lit` — literature: novelty, build-on, support/contradict, and mining comparison values
- `/paper-frame` — Introduction, Conclusions, Abstract, Title, from the established body
- `/paper-finish` — sweep the gaps, fill the references, check the venue, build

`/paper-iterate`, `/paper-frame` and `/paper-finish` are the remaining phases.

## Using it

Install once, globally: this repo is composed into a shared agent home (the `ai-agent-home` repo) as a manifest-managed clone, which links every `skills/*/SKILL.md` into the one catalogue each harness reads. The skills are then available from any working directory.

`/paper-start` scaffolds a paper **workspace** — always `sci-paper-workspace/`, a fixed-name subdirectory of wherever you are, and always its own independent git repository. Nothing sci-paper creates or touches ever reaches the project's own git history: your working directory's `CLAUDE.md` gets one small appended index block, and its `.gitignore` gets one appended line excluding the workspace entirely. Everything the paper needs — its draft, its memory, its literature notes, an optional `paper-voice/` of past papers to write like — lives inside that one isolated directory, found and read relative to it; your own `notes/`, `figures/` and `code/` stay exactly where your project already keeps them.

Between sessions the project remembers itself in `paper/` — a short living state file, an append-only journal, the argument spine, open questions, and literature notes. A new conversation picks up where the last one stopped.

Needs an [ADS/SciX API token](https://ui.adsabs.harvard.edu/user/settings/token) and `latexmk`. No third-party Python packages, no node, no MCP client.

## Licence

MIT
