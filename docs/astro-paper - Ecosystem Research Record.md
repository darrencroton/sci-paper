# astro-paper — Phase 1/2 research record

Compiled 2026-08-18. All repositories inspected at the commit current on that date via `gh api` (file trees + raw file contents), not from READMEs alone.

## Projects inspected

| Repo | Stars | Last push | Size | Licence | What it actually is |
|---|---:|---|---:|---|---|
| SNL-UCSB/paper-writing-skill | 165 | 2026-07-31 | 312 KB | MIT | One large SKILL.md (34 KB) + `author_profile/` style layer + per-section rhetorical-move refs + brainstorming guide. CS/systems venues. |
| SNL-UCSB/literature-survey-skill | 71 | 2026-03-27 | 73 KB | MIT | Intent → triage → deepen → synthesise. Templates only; NotebookLM-oriented, no API backend. |
| SFETNI/Scientific-Writing-Skills-Claude-Code-Codex | 2 | 2026-06-26 | 5.2 MB | custom | 24 micro-skill `.md` files + 10 slash commands + 6 state templates + 1 checker script + full synthetic example. Biomed/ML framing. |
| skymanbp/sci-paper | 4 | 2026-08-17 | 1.3 MB | custom | 8 skills + 24 Python tools (~350 KB) + 51 KB normative standard + trained voice/AI-ism models. Bilingual zh/en. Targets ApJ/MNRAS/PRD/JCAP. |
| PoseZhaoyutao/research-paper-writer-skill | 2 | 2026-05-19 | 35 KB | none | Codex skill; `collect_paper_context.py` (repo scan) + `audit_evidence_manifest.py`. |
| K-Dense-AI/scientific-agent-skills | 33.7 k | 2026-08-17 | 247 MB | MIT | 161 skills, overwhelmingly bio/chem. Relevant: `scientific-writing`, `peer-review`, `uncertainty-and-units`, `citation-management`, `astropy`. |
| SukiYume/nasa-ads-skill | 2 | 2026-07-29 | 185 KB | MIT | Best-designed ADS skill: 12 KB SKILL.md + 19 KB stdlib-only CLI + 13 KB tests. Claude/Codex/Gemini plugin packaging. |
| gnarayan/ads-cite | 3 | 2026-05-24 | — | MIT | Written by a working astronomer. 41 KB `ads_cite.py`. Verbatim BibTeX, citekey rekeying, refereed-preference resolution. |
| adsabs/scix-mcp | 4 | 2026-08-14 | — | MIT | **Official** ADS/SciX MCP server (TypeScript). `SCIX_API_TOKEN`, `SCIX_API_BASE`. |
| OpenRaiser/PaperFit | 320 | 2026-06-22 | — | — | LaTeX typesetting agent: compile → render → diagnose → fix layout. 5 sub-agents. |
| Future-House/paper-qa | 9046 | 2026-08-12 | — | Apache | Full-text RAG with citations. 16 core deps incl. own LLM stack (fhlmi/litellm), tantivy, tiktoken. |
| hanlulong/econ-writing-skill | 541 | 2026-07-20 | — | — | Field-specific writing skill; single 54 KB SKILL.md + 4 refs. Most-starred field writing skill. |
| xnchu/ads-paper-search, YifZhou/ads-bib, RuancunLi/astroskills, ShaishavMaisuria/research-paper-lifecycle-skills | — | 2026 | — | mixed | Smaller/adjacent; skimmed. |

## Comparison matrix

Legend: ● strong · ◐ partial · ○ absent · ✗ actively wrong for our purpose

| Dimension | SNL-UCSB pws | SFETNI | sci-paper | PoseZhaoyutao | K-Dense | SukiYume ADS | ads-cite | PaperQA2 |
|---|---|---|---|---|---|---|---|---|
| Scope | draft pipeline | QC framework | review+standard | draft w/ agents | component library | literature backend | citation fetch | full-text QA |
| Assumes analysis complete | ○ (pre-eval Draft 0) | ● explicit | ● | ◐ | ◐ | n/a | n/a | n/a |
| Human/agent boundary stated | ● | ● 4 gates | ● dispositions | ◐ | ● | ● | ● | ○ |
| Composability | ◐ monolith+refs | ● 24 units | ◐ 8 large | ○ | ● | ● | ● | n/a |
| Repo ingestion | ○ | ○ | ○ | ◐ only real attempt | ○ | n/a | n/a | ○ |
| Provenance figure→script→data | ○ | ○ | ◐ prose rule only | ○ | ◐ asserted | n/a | n/a | ○ |
| Persistent state | ◐ 1 MD file | ● 6 MD templates | ○ (style profile only) | ◐ manifest | ● JSON/CSV | ○ | ○ | ○ |
| Claim/evidence model | ◐ prose | ● labels+register | ◐ review-time lists | ◐ manifest | ● E/C/N/M/O/R IDs | ○ | ○ | ◐ contexts |
| Alternative interpretations first-class | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Numerical provenance | ○ | ● but degenerates | ● prose rule | ◐ | ● | ○ | ○ | ○ |
| Uncertainty/units structured | ○ | ○ | ◐ | ○ | ◐ | ○ | ○ | ○ |
| Literature backend | ○ | ○ web search | ◐ arXiv fetch | ○ | ◐ OpenAlex/PubMed/Scholar | ● ADS | ● ADS | ● multi |
| Refereed filtering (authoritative) | ○ | ○ | ○ | ○ | ○ | ● `property:refereed` | ● doctype filter | ○ |
| Citation verification ladder | ○ | ● 4-level | ◐ existence+relevance | ◐ | ● human-verified IDs | ○ | ○ | ◐ |
| Figure integration | ◐ synthesis | ◐ QC checklist | ● best in class | ○ | ◐ | n/a | n/a | ○ |
| Compiled-page visual review | ○ | ○ | ● 150 DPI | ○ | ○ | n/a | n/a | ○ |
| LaTeX support | ◐ tikz | ◐ paths+cites | ● build+length gates | ◐ | ✗ removed on purpose | ● export fmts | ● bibtex | ○ |
| Human checkpoints | ● red-team loop | ● 4 named gates | ● dispositions | ◐ | ● approval flags | ● confirm-destructive | ● pick-result | ○ |
| Iterative collaboration | ● loop mode | ◐ per-phase | ● measure/re-measure | ◐ | ◐ | n/a | n/a | ○ |
| Reviewer architecture | ◐ red-team persona | ● 6 subagent templates | ● isolated MPR | ● multi-agent mandated | ● lint+scaffold | n/a | n/a | ○ |
| Deterministic checks | ◐ grep gate | ◐ 1 script, 5 checks | ● 24 tools + tests | ◐ 1 audit script | ● 8 dep-free scripts | ● CLI + tests | ● CLI + tests | ● |
| Anti-self-certification | ● evidence-gated | ◐ fail conditions | ● measurement states | ● adversarial | ◐ | ● negative calibration | ○ | ○ |
| Astronomy specificity | ○ | ○ | ◐ + author's own field | ○ | ◐ astropy only | ● | ● | ○ |
| Claude Code compat | ● | ● | ● plugin | ◐ Codex-first | ● | ● | ● | n/a lib |
| Codex compat | ◐ | ● CODEX.md | ○ | ● | ● | ● | ○ | n/a |
| Maintenance burden | low | medium | **very high** | low | high | low | low | external |
| Dependencies | none | none | numpy/sklearn/torch-ish | none | none | **stdlib only** | stdlib+ | 16 pkgs |

## Evidence for the key judgements

### 1. "Every decimal must be registered" degenerates — proven by its own example

`SFETNI/scripts/check_manuscript_integrity.py:186-226` greps `\b(\d+\.\d+)\b` from the `.tex` and warns for any token absent from `NUMERICAL_REGISTRY.md`. Their own worked example then had to add a **"Decimal Coverage Tokens"** section with 40+ junk rows to silence it (`example/NUMERICAL_REGISTRY.md:75-120`), including:

- `COV020 | 0.78 | ... | 03_results.tex:25,37,46,58` — a `width=0.78\textwidth` option
- `COV026 | 0.95`, `COV012 | 0.1`, `COV007 | 0.000`

The registry is polluted to appease the checker. The header even concedes it: *"Some entries below are formatting parameters or table-only descriptive values; they are included to keep the mechanical audit explicit."* Conclusion: number checking must be **claim-directed and LaTeX-aware**, not token-directed, and unregistered numbers must be a triage list with a persistent classification file — never a hard demand.

### 2. Style bans leak into integrity

`check_manuscript_integrity.py:31-57` banned-phrase list includes bare `"leverage"`, `"utilize"`, `"facilitate"`, matched as lowercased substrings. In astronomy *leverage* is a regression diagnostic; the check would flag legitimate statistical prose. sci-paper goes further with a "zero-target L0 lexicon" including an em-dash ban and second-use bans on Tier B words, enforced by a trained classifier (`tools/ai_ism_lint.py`, `tools/train_ai_ism_classifier.py`). This is author taste enforced as a hard gate.

### 3. Two projects independently found the same failure mode: self-certification

- SNL-UCSB `DESIGN.md:96-100`: *"A live-review audit found the failure mode was not too few rules but self-certification — the agent that wrote the prose graded its own audit and skipped the greps. So review is independent…, evidence-gated (paste the grep output, not 'audited'), and loopable to closure."*
- sci-paper `paper-review/SKILL.md:44-48`: *"缺失测量不等于 0"* — every axis explicitly `measured` / `degraded` / `unmeasured` / `not_applicable`; **no PASS verdict**; *"grep 只定位"* — a grep hit or miss is never semantic evidence.

Convergent evidence from two unrelated codebases. This is a first-class architectural requirement, not a nicety.

### 4. ADS/SciX transition is cheap to absorb

- `https://api.adsabs.harvard.edu/v1/search/query` → HTTP 401
- `https://api.scixplorer.org/v1/search/query` → HTTP **401** (not 404)

Same v1 Solr path surface on both hosts. The official `adsabs/scix-mcp` confirms it: `SCIX_API_BASE` *"(optional): override the API base URL. Defaults to `https://api.adsabs.harvard.edu/v1` when unset."* A single configurable base URL + token-env resolution order is the whole abstraction. A heavyweight `AstronomyLiteratureBackend` class hierarchy is not warranted.

### 5. Authoritative ADS metadata for our integrity invariants

From `adsabs/adsabs.github.io` docs source (not the JS-rendered site):

- `property:refereed` / `property:notrefereed` — **authoritative peer-review flag.** This is how invariant #8 (never infer peer review from arXiv presence) becomes mechanical rather than aspirational.
- `property:article` / `nonarticle`; `openaccess`, `pub_openaccess`, `eprint_openaccess`, `ads_openaccess`, `author_openaccess`, `esource` (full-text reachability → gates the top of the verification ladder); `data` (paper has data links); `inspire`.
- `doctype`: abstract, article, book, bookreview, catalog, circular, editorial, eprint, erratum, inbook, inproceedings, mastersthesis, misc, newsletter, obituary, pressrelease, proceedings, proposal, software, talk, techreport.
- `database:astronomy|physics|general`.
- Second-order operators: `citations()`, `references()`, `reviews()`, `similar()`, `useful()`, `topn()`, `trending()`.
- `object:` — SIMBAD/NED-tagged object search **and cone search**; plus `nedid`, `nedtype`, `ned_object_facet_hier`.
- `bibgroup:` — curated telescope/institutional bibliographies (e.g. per-observatory).
- `orcid`, `orcid_pub`, `orcid_user`, `orcid_other`; `inst:` with parent/child canonical affiliations.

`reviews()` and `topn()` are directly useful for the "foundational vs recent" requirement.

### 6. Practical astronomy citation mechanics — from the astronomer-authored skill

`gnarayan/ads-cite/SKILL.md`:
- *"Do NOT hand-edit or fabricate bibtex — it comes verbatim from the ADS export endpoint."*
- Default search filters `database:astronomy`, `doctype:(article OR eprint)` — excludes AAS meeting abstracts, proceedings, theses.
- arXiv/DOI resolution *"prefers refereed version if one exists"*.
- **Citekey rekeying** (`LastName_Subject_Year`), collision detection, `--rekey-report` dry run, low-confidence WARNs, collaboration-author tags, and *"if the target .bib already has entries keyed by raw bibcode, match that convention"*. This is real friction nobody else models.
- Token resolution: macOS Keychain → `ADS_DEV_KEY`/`ADS_API_TOKEN` → `~/.ads/dev_key`, explicitly so it works on NERSC/NCSA-style HPC.

### 7. Journal profiles must be versioned data, not prose in a SKILL.md

- AASTeX **v7.0.1** (v7.0 released 2025-03-04); new `.bst` changing inline citations to first-initial form ("G. Smith et al. 2022"); new author-contribution environment.
- MNRAS `mnras.cls` **v3.3** (April 2024) + `mnras.bst`; guidance against `amssymb` with `newtxmath`.
- A&A `aa.cls` macro package **v9.4** (March 2026). A&A **returns AASTeX-formatted or generic-article submissions before peer review** — a hard constraint.

Three venues, three different current versions, one changed in the last six months. Baking these into prose guarantees staleness.

### 8. Environment constraints measured on this machine

| Fact | Value | Consequence |
|---|---|---|
| `python3` | 3.14.6 | modern stdlib: `tomllib`, `sqlite3` present |
| third-party packages | **none** — no numpy, yaml, requests, astropy, PIL, pymupdf | tools must be stdlib-only, or use a repo-local venv |
| `uv` | present | clean venv/PEP-723 path available |
| LaTeX | `pdflatex`, `xelatex`, `latexmk` | build + compile checks feasible |
| PDF raster | `pdftoppm`, `pdfinfo`, `gs`, `sips` | **150 DPI page rendering without pymupdf** — sci-paper's best idea, zero deps |
| `gh`, `jq`, `git` | present | — |

## Adopt / adapt / build / reject

**Adopt near-verbatim (with attribution):**
1. Stdlib-only ADS CLI shape, token-env resolution, redirect rejection, no-token-on-argv, `numFound` ≠ relevance, negative-result calibration, query families + coverage standard — *SukiYume*.
2. Verbatim-BibTeX rule, refereed-preference resolution, default astronomy doctype filters, citekey rekeying with dry-run — *ads-cite*.
3. Measurement-state axes, typed findings (`integrity_blocker` / `advisory`), no-PASS verdict, "grep only locates", re-gather evidence each round, advisory dispositions (`acted`/`accepted`/`rejected_as_false_positive`/`pending`) — *sci-paper*.
4. Compiled-page review at 150 DPI; fix at the generator not the caption; cross-figure encoding consistency; anti-patterns list — *sci-paper figure-review*.
5. Evidence-gated independent review (paste the tool output, not "audited"); loop-to-closure — *SNL-UCSB*.
6. Explicit missing/unverified/not-applicable state instead of plausible boilerplate; dependency-free, network-free, deterministic scripts — *K-Dense*.

**Adapt:**
7. Citation verification ladder — *SFETNI*, but re-anchor `METADATA_VERIFIED` to "matched to an ADS record" and insert `REFEREED_CONFIRMED`; and move the ladder from the *paper* to the *(paper, claim) edge*.
8. Claim evidence labels (`RESULT_SUPPORTED` / `LITERATURE_SUPPORTED` / `METHOD_DEFINITION` / `INTERPRETATION` / `SPECULATION` / `UNSUPPORTED` / `NEEDS_HUMAN_DECISION`) — *SFETNI*.
9. Numerical registry — *SFETNI*, redesigned bidirectionally, LaTeX-aware, with a persistent ignore/classification file.
10. Named human gates — *SFETNI*, but continuous rather than 4 checkpoints.
11. One writing pipeline + per-section rhetorical-move reference files — *SNL-UCSB*; "introduction constrained by what the results actually show" survives, "Draft 0 before evaluation" does not apply to a finished analysis.
12. Repo scan — *PoseZhaoyutao*, rewritten: astronomy formats, git-aware, provenance edges, JSON output, size guards, no Codex-session scraping.
13. ID registries — *K-Dense*, collapsed from six namespaces to four.

**Build ourselves (genuine gaps):**
14. Provenance graph: figure/table → generating script → input data, with per-edge evidence and confidence.
15. Two-layer state: machine-discovered (regenerable) vs author-approved (durable) — makes staleness detectable.
16. Alternative interpretations and caveats as first-class objects attached to claims.
17. Claim `strength` as an enum that prose must not exceed.
18. Structured value objects: value + uncertainty (symmetric/asymmetric/upper-limit) + unit, including dex and log-quantities.
19. Astronomy consistency checks: cosmology parameters, redshift ranges, sample cuts, IMF/magnitude systems, object naming.
20. The join nobody has built: ADS evidence ↔ manuscript claim ↔ author approval.

**Reject:**
21. Six ID namespaces; hashing claim text (destroys human editability).
22. One skill per manuscript section — the procedure is identical, only the rhetorical moves differ; that is data.
23. Trained voice models / AI-ism classifiers / zero-target lexicons / em-dash bans.
24. "Every decimal must be registered."
25. Reporting-guideline machinery (CONSORT/PRISMA/STROBE) — no astronomy analogue.
26. 20-database literature federation. ADS is field-comprehensive; Crossref/OpenAlex only as a metadata cross-check.
27. MCP dependency for ADS. A ~300-line stdlib client is simpler, testable and repo-contained; document `adsabs/scix-mcp` as an optional alternative transport.
28. PaperQA2 as a dependency — 16 packages and its own LLM/embedding stack to solve a small-N problem (5–30 key citations) that direct PDF reading handles better.
29. Bilingual skill files; roleplaying six reviewers in one context window.
