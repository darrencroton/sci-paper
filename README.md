# astro-paper

**Work in progress — build under way.**

A small set of [Claude Code](https://claude.com/claude-code) skills that help a working astronomer turn notes, figures, tables and analysis code into a journal paper — and then keep working on it for as long as it takes.

It is built for the way papers actually get written: **starting before the picture is complete, and letting the writing shape the result.** The first draft it produces is deliberately incomplete, with every hole marked rather than smoothed over. From there it iterates with you — suggesting connections, hunting the literature for supporting and contradicting work, filling references — and writes the Introduction and Conclusions last, once there is something to introduce and conclude.

The astronomer is the verifier. The system never claims a number, method or citation is correct; it makes what it did visible and traceable so you can check it fast.

## Status

| | |
|---|---|
| Design | complete — see [`docs/astro-paper - Plan.md`](docs/astro-paper%20-%20Plan.md) |
| Implementation | **P3 done.** `/paper-start` and `/paper-draft` take a real `notes/` + `figures/` + `code/` directory to a compiling, honestly-incomplete body draft; `tools/ads.py` and `/paper-lit` add the literature arm — novelty, build-on, support/contradict and mining, with BibTeX verbatim from ADS. P4 (`/paper-iterate`) next |

## What is here

```text
docs/
├── astro-paper - Plan.md                        # the design. start here
├── astro-paper - Corpus Evidence.md             # measurements over six published papers
└── astro-paper - Ecosystem Research Record.md   # survey of ~14 comparable projects + ADS API facts
tools/ads.py                                     # the only script: ADS/SciX, stdlib only
skills/
├── _shared/
│   ├── memory.md                                # what to read first, what to write last, paper/lit/
│   ├── house-rules.md                           # integrity rules, gap markers, % src:, editing
│   └── sections/                                # rhetorical moves per section role — data, not skills
├── paper-start/SKILL.md                         # ingest, look at the figures, propose the argument
├── paper-draft/SKILL.md                         # write one section; mark what it cannot answer
└── paper-lit/SKILL.md                           # query craft and the four literature modes
skeleton/                                        # copied into a paper repo by /paper-start
├── CLAUDE.md
├── paper/                                       # STATE, journal, outline, open questions, lit
└── manuscript/                                  # main.tex + astropaper.sty
```

## Shape of it

Six skills, one 396-line stdlib script for ADS access, and a 124-line LaTeX package — the gap-marker macro plus the AAS journal abbreviations that verbatim ADS BibTeX needs. No MCP servers, no databases, no schemas. Almost all the value is in how specific the skill files are, not in the code.

- `/paper-start` — read the notes, look at the figures, propose an argument and a list of questions
- `/paper-draft` — write a section from notes, code or figures; mark what it cannot answer
- `/paper-iterate` — the thinking loop: connections, tensions, buried leads, ordering
- `/paper-lit` — literature: novelty, build-on, support/contradict, and mining comparison values
- `/paper-frame` — Introduction, Conclusions, Abstract, Title, from the established body
- `/paper-finish` — sweep the gaps, fill the references, check the venue, build

Between sessions the project remembers itself in `paper/` — a short living state file, an append-only journal, the argument spine, open questions, and literature notes. A new conversation picks up where the last one stopped.

## Licence

MIT
