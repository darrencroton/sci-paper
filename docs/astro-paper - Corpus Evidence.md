# Corpus evidence — measurements behind the astro-paper plan

> **Status note (2026-08-21).** This document is **historical evidence for the design**, not a component specification. It was written against an abandoned earlier design, and its cross-references to plan sections and to components such as `texparse.py` and `check_interfaces.py` describe *that* plan — none of them exist in the current plan. The measurements themselves remain valid and are why the current design retires this corpus as a foundation (see Plan §10).

*Aligned to plan v5.1. Measurements re-derived twice after external review: once to replace regex-agreement with syntactic ground truth, and once to remove `\citeauthoryear` contamination and add the sixth paper to the manifest.*

These are the empirical measurements that drove the plan's revisions. Audit the **methodology and the inferences drawn**, not just the numbers.

## Corpus

**Six** published papers by the plan's author, under `~/Documents/Science/papers/Mine/completed/` (outside the review repo; paths given for provenance). The **file manifest is frozen at 19 `.tex` files**: one per paper except `2016-sage-paper`, which contributes all 14 `\input` sections. (An earlier revision stated 18 files and omitted `2011_mutch_MW_GreenValley` entirely while still describing a six-paper corpus; that omission is corrected here.) Every measurement below uses this same manifest unless stated.

| Dir | Type | Class | Notes |
|---|---|---|---|
| `2006_croton_AGN` | semi-analytic model | `mn2e` | MNRAS 365, 11. **Has a published erratum.** |
| `2004_croton_HigherOrders` | measurement (2dFGRS counts-in-cells) | `mn2e` | inline `thebibliography`, prose citations |
| `2013_croton_little_h` | pedagogical/methods | `article` | PASA; has `.py` generators + `.txt` data |
| `2016-sage-paper` | code release | `emulateapj` | ApJS; `\input{section01..14}`; 102 git commits |
| `2011_mutch_MW_GreenValley` | student-led | `article` | Science submission format; `v8/ v10/ old/` |
| `2008_croton_voids` | measurement | `mn2e` | `\bibliography{../paper}` — .bib above the manuscript dir |

## Measurement 1 — citation-extraction recall (ground truth)

**Method.** Ground truth is obtained by *enumerating every cite-family invocation syntactically*, not by comparing two regexes. The construct is syntactically decidable, so exhaustive command enumeration **is** the gold set; no manual annotation is required or claimed.

```python
CITE = re.compile(r"\\(cite|citet|citep|citealt|citealp|citeauthor|citeyear|citeyearpar"
                  r"|citenum|citetext|Citet|Citep|Citealt|Citealp|Citeauthor)"
                  r"(\*?)((?:\[[^\]]*\])*)\{([^}]*)\}")     # ground-truth enumerator
NAIVE = re.compile(r"\\cite[tp]?\*?\{")                                  # reference implementation
# comments stripped with re.sub(r"(?<!\\)%[^\n]*", "", text) first
```

An invocation counts as *matched* when `NAIVE.match()` succeeds on the enumerated invocation text.

Two exclusions, both material:
- **Only the document body is scanned.** Everything from `\begin{thebibliography}` onward is excluded.
- **`\citeauthoryear` is not a citation.** It is a natbib *bibliography-label* helper appearing inside `\bibitem`:
  `\bibitem[\protect\citeauthoryear{Blake et al.}{2011}]{Blake2011}`. All 27 occurrences are inside `2013_croton_little_h`'s inline `thebibliography`. Counting them as manuscript citations inflated an earlier denominator.

| Quantity | Value |
|---|---:|
| Files measured | 19 (frozen manifest, 6 papers) |
| Ground-truth citation invocations (body only) | **439** |
| Matched by the reference regex | **336 (76.5%)** |
| **Structurally unmatchable** | **103 (23.5%)** |

Forms present, by frequency: `cite` 169, `citep` 96, `citet` 67, `citep[opt]` 53, `citealt` 27, `citep*[opt]` 7, `citealt*` 5, `citet[opt]` 5, `citeauthor` 4, `citet*` 3, `cite[opt]` 2, `citep*` 1 — twelve distinct forms.

The reference pattern `\cite[tp]?\*?\{` cannot match any optional-argument form (`\citep[e.g.][]{...}`) or any command outside `{cite, citet, citep}` (`\citealt`, `\citealp`, `\citeauthor`). This is a **structural** limit provable from the pattern, not a sampling artefact.

Key-level example (`2008_croton_voids`): 15 unique keys recovered by the reference regex against 37 actually cited — 40.5%.

**Corrections applied.** An early revision reported "61.8% recall" from a 6-file subset — that was agreement between two regexes, not recall. A later revision reported 67.7% but counted `\citeauthoryear` label helpers as citations and omitted the sixth paper. The figure above (76.5%) is the corrected value. The conclusion is unchanged in direction and remains decisive: roughly **one citation invocation in four** is structurally invisible to the reference pattern, and `2004_croton_HigherOrders` is invisible to *any* key-based approach.

## Measurement 2 — figure-inclusion macro distribution

**Method.** Counts **invocations**, defined as a figure command followed by an optional bracket group then `{`. Macro *definitions* (`\newcommand{\plotone}[1]{...}`) are excluded — v2.0 wrongly counted them, which inflated the legacy-macro share. Asset slots equal invocations here because no multi-image macro (`\plottwo`, `\plotthree`) is invoked anywhere in the manifest, though five are *defined*.

| Macro | Invocations |
|---|---:|
| `\psfig` | 20 |
| `\plotone` | 18 |
| `\includegraphics` | **23** |
| `\plotfull` | 5 |
| `\plotscaled` | 1 |
| **Total** | **67** |

`\includegraphics` is **34.3%** of invocations; an `\includegraphics`-only checker misses **65.7%**.

Per paper — the distribution is bimodal, which matters more than the aggregate:

| Paper | `\includegraphics` | legacy/user macros | total |
|---|---:|---:|---:|
| 2006_croton_AGN | **0** | 19 | 19 |
| 2004_croton_HigherOrders | **0** | 16 | 16 |
| 2008_croton_voids | **0** | 9 | 9 |
| 2013_croton_little_h | 3 | 0 | 3 |
| 2016-sage-paper (14 sections) | 11 | 0 | 11 |
| 2011_mutch_MW_GreenValley | 9 | 0 | 9 |

**Three of six papers contain zero `\includegraphics`.** Every figure in them resolves through a user macro wrapping `\psfig`:

```latex
\newcommand{\plotone}[1]{\centering \leavevmode \psfig{file=#1,width=\columnwidth,clip=}}
```

**Corrections applied.** An early revision reported 6% from a subset that under-sampled `2016-sage-paper` and counted macro *definitions* as invocations; a later revision reported 24.1% but omitted `2011_mutch_MW_GreenValley`. The corrected figure is 34.3%. **The per-paper split is the finding that matters**: three of six papers are entirely invisible to an `\includegraphics`-only checker, and the aggregate percentage understates that.

## Measurement 3 — bibliography mechanism

| Paper | Mechanism |
|---|---|
| 2004_croton_HigherOrders | inline `\begin{thebibliography}`, **73 `\bibitem`**, **0 `\cite`**, prose citations ("Norberg et al. 2001") |
| 2008_croton_voids | `\bibliography{../paper}` — **.bib lives above the manuscript directory** |
| 2006_croton_AGN | `.bbl` shipped alongside `.tex` |

A `\cite`-keyed checker reports **"0 citations, all valid"** for the first paper. This drove the zero-finding guard (plan §3.1).

## Measurement 4 — table number density

`2004_croton_HigherOrders` results table, one representative row:

```latex
1 & 0.71 & 7.1 & $2.58\pm0.37 \,(0.1) $ & $9.3\pm4.0 \,(0.1) $ & $34\pm32 \,(0.1)$ & $---$ & $0.96\pm0.16 \,(0.1)$ & $0.17\pm0.25 \,(0.1)$\\
```

Counted exactly: the results table contains **108 numeric tokens** (71 decimal, 37 integer); the companion VLC table contains **90** (52 decimal, 38 integer) — **198 across the two tables**. Under v1.0's "every decimal must be registered" direction-2 check, all become findings. This reproduces the failure visible in the reference implementation's own worked example, where `example/NUMERICAL_REGISTRY.md:75-120` carries 40+ "Decimal Coverage Tokens" rows — including `0.78` (a `width=0.78\textwidth` option) — added purely to silence the checker.

Also present: `$---$` as a legitimate "no reliable measurement" marker, and bare `$1$`/`$0$` for the reference sample.

## Measurement 5 — little-h scaling density

Single table header, `2004_croton_HigherOrders`:

```latex
{\tiny $M_{b_{\rm J}}-5\log_{10}h$}   {\tiny $10^{-3} h^3$Mpc$^{-3}$}   {\tiny $h^{-1}$Mpc}   {\tiny $10^6h^{-3}$Mpc$^3$}
```

**Three distinct powers of $h$** ($+3$, $-1$, $-3$) plus a $5\log_{10}h$ magnitude convention, in one header. (v2.0 said "four"; the plan body said "five". Both were wrong.) Cosmology is declared **in the table caption** (`$\Omega_m=0.3$, $\Omega_\Lambda=0.7$`), not in a Methods section.

## Measurement 6 — provenance obstacles (`2013_croton_little_h`)

```python
# hubble-diagram.py
OutputFormat = '.pdf'                                    # line 33
plt.savefig(outputFile)                                  # line 144
print 'Saved file to', outputFile                        # line 145  <- Python 2
outputFile = '/Users/dcroton/Documents/Papers/current/croton_little_h/' + OutputFileName + OutputFormat   # line 159
```

- `ast.parse()` raises `SyntaxError` on line 145 (Python 2 print).
- `savefig` argument is a variable, not a literal.
- The absolute path points at a directory that no longer exists (repo has since moved).
- Script writes `.pdf`; the manuscript includes `./hubble_diagram.eps`.
- Sibling artifacts present: `hubble_diagram.eps`, `hubble_diagram.pdf`, `hubble_diagram_2.pdf`.
- `F2.large.eps` exists but its `\includegraphics` is commented out (orphan asset).
- `hubble/` mixes data (`galaxies.txt`, `groups.txt`, `hubble1929.gc`) with downloaded literature PDFs (`1004.1711v1.pdf`, `PNAS-1929-Hubble-168-73.pdf`).
- Repo root contains `croton_little_h.pdf` — the compiled output of the paper itself.

## Measurement 7 — the erratum

`2006_croton_AGN/submit_erratum/croton_AGN_erratum.tex:58-74`, verbatim:

> "In preparing the script to plot the Tully-Fisher relation in Figure~6 ... we inadvertently loaded the incorrect column from our database with the result that the proxy $V_{\rm c}$ is not the virial velocity of the parent dark matter halo, $V_{\rm vir}$, as labeled, but is instead the maximum circular velocity of the dark matter halo, $V_{\rm max}$. ... This confusion influenced the discussion of the Tully-Fisher relation in our paper. In fact, Figure~6 demonstrates that it is possible to simultaneously reproduce both the local Tully-Fisher relation and luminosity function ... thus contradicting previous studies of this issue and our own discussion in Section~3.6."

A wrong database column → a mislabelled axis → a **wrong published scientific conclusion**, in a paper with several thousand citations, caught only after publication by an external reader.

This motivated an automated axis↔column checker in an earlier plan revision. That tool was **removed** (see plan §6.3 and §16): it requires provenance to bind a *named* column to a specific axis, which Measurement 9 shows is often impossible, and if the expected symbol is derived from the generator the comparison is a tautology. The plan now treats this as evidence presented for author judgement, with an explicit `unmeasured` when the binding cannot be resolved.

## Measurement 8 — section headings are not canonical

| Paper | Headings |
|---|---|
| 2006_croton_AGN | Introduction / The dark matter skeleton: the Millennium Run / Building galaxies: the semi-analytic model / Results / **Physical models of AGN feedback** (= Discussion) / Conclusions |
| 2008_croton_voids | Introduction / The Galaxy Formation Model / Estimating local densities / **Results and Discussion** (combined) / Summary |
| 2004_croton_HigherOrders | Introduction / Count-in-Cells Statistics / Application to the 2dFGRS / Results / Interpretation and the implications for galaxy bias / Conclusions |
| 2013_croton_little_h | 8 sections, **no Results section at all** |
| 2011_mutch_MW_GreenValley | `\section*{Supporting Online Material.}` only (Science format) |

No paper in the corpus uses a "Methods" heading. None has a "Limitations" section.

## Measurement 9 — data embedded in the generator

`2013_croton_little_h/model-smf.py` hard-codes its data as an inline Python literal:

```python
[7.05, 1.3531e-01, 6.0741e-02],
[7.15, 1.3474e-01, 6.0109e-02],
...
```

There is no input file and there are no column *names* — only positional array entries. Any check that compares a figure axis symbol to a named data column is `unmeasured` here by construction. This is why the plan does not assert an automated axis↔column check, and why provenance records how the data reference was obtained (named column, positional index, inline literal, or unresolved) rather than pretending it always resolves.

## Questions this evidence was used to answer

1. Are any of the eight measurements methodologically unsound, or do they support conclusions they do not warrant?
2. Is `texparse.py` (§7.1) the right consolidation, or does a single shared parser create an unacceptable single point of failure?
3. Is `check_interfaces.py` (§5.6) genuinely able to catch the Measurement-7 class, or is the claim overstated given that provenance must first resolve the column?
4. Does the plan add complexity that will not pay for itself? Name specific components to cut.
5. What failure mode present in this corpus does the plan still not address?
