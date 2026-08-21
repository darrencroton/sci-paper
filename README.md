# astro-paper

**Work in progress — design stage. Nothing is built yet.**

A small set of [Claude Code](https://claude.com/claude-code) skills that help a working astronomer turn notes, figures, tables and analysis code into a journal paper — and then keep working on it for as long as it takes.

It is built for the way papers actually get written: **starting before the picture is complete, and letting the writing shape the result.** The first draft it produces is deliberately incomplete, with every hole marked rather than smoothed over. From there it iterates with you — suggesting connections, hunting the literature for supporting and contradicting work, filling references — and writes the Introduction and Conclusions last, once there is something to introduce and conclude.

The astronomer is the verifier. The system never claims a number, method or citation is correct; it makes what it did visible and traceable so you can check it fast.

## Status

| | |
|---|---|
| Design | complete — see [`docs/astro-paper - Plan.md`](docs/astro-paper%20-%20Plan.md) |
| Implementation | not started |

## What is here

```
docs/
├── astro-paper - Plan.md                        # the design. start here
├── astro-paper - Corpus Evidence.md             # measurements over six published papers
└── astro-paper - Ecosystem Research Record.md   # survey of ~14 comparable projects + ADS API facts
```

## Shape of it

Six skills, one ~200-line stdlib script for ADS access, and a ~25-line LaTeX package. No MCP servers, no databases, no schemas. Almost all the value is in how specific the skill files are, not in the code.

- `/paper-start` — read the notes, look at the figures, propose an argument and a list of questions
- `/paper-draft` — write a section from notes, code or figures; mark what it cannot answer
- `/paper-iterate` — the thinking loop: connections, tensions, buried leads, ordering
- `/paper-lit` — literature: novelty, build-on, support/contradict, and mining comparison values
- `/paper-frame` — Introduction, Conclusions, Abstract, Title, from the established body
- `/paper-finish` — sweep the gaps, fill the references, check the venue, build

Between sessions the project remembers itself in `paper/` — a short living state file, an append-only journal, the argument spine, open questions, and literature notes. A new conversation picks up where the last one stopped.

## Licence

MIT
