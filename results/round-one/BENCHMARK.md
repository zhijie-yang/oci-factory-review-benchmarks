# Code-review skill comparison

Run: 2026-10-16, PATS v0.7.2, OpenCode 1.19.3,
OpenRouter anthropic/claude-haiku-4.5, three concurrent tasks.
One execution per version/case, 12 cases, 36 completed reviews and 144 scoring
cells. All preflights passed, every task exited zero, and full-matrix audit passed.
All 36 Markdown and JSON reviews were inspected after automated scoring.

## Results

| Metric | Original 63a27d3b | PPA e996ff5e | Both changes 508d7346 |
| --- | ---: | ---: | ---: |
| Raw PATS aggregate | 65.6% | 74.0% | 76.0% |
| Actual verdict matches, independently of schema | 9/12 | 9/12 | 10/12 |
| Expected blocker cases detected | 6/6 | 6/6 | 6/6 |
| Nonblocking cases incorrectly blocked | 3/6 | 3/6 | 2/6 |
| Exact findings scorer | 7/12 | 8/12 | 8/12 |
| Gate assertions matching oracle | 38/48 | 38/48 | 38/48 |
| Recipe-summary scorer | 6/12 | 9/12 | 10/12 |
| Reported task cost | $0.3534 | $0.3347 | $0.3301 |

Total reported task cost: $1.0182, excluding three credential preflights.
Summed task duration: 1409.1 seconds (not wall-clock time; tasks ran in parallel).
Costs are harness-reported, not reconciled against an OpenRouter invoice.

The final variant improved raw aggregate by 10.4 percentage points over baseline,
but mainly through better structured reporting. Substantive verdict accuracy rose
from 75.0% to 83.3%, only one additional correct case. No variant missed a required
blocker; all detected the package, slice and permission runtime failures even
before the broader regression guidance. There is no demonstrated detection gain
on those three cases in this run.

## Per-case verdicts

| Case | Expected | Original | PPA | Both |
| --- | --- | --- | --- | --- |
| 01 PPA declaration, unknown provenance | Comment | Request changes | Request changes | Request changes |
| 02 Direct-source EOL violation | Request changes | Request changes | Request changes | Request changes |
| 03 Unconfirmed part removal | Request changes | Request changes | Request changes | Request changes |
| 04 Unconfirmed service removal | Request changes | Request changes | Request changes | Request changes |
| 05 Confirmed harmless removal | Approve | Approve | Approve | Approve |
| 06 Missing startup executable | Request changes | Request changes | Request changes | Request changes |
| 07 Missing required library | Request changes | Request changes | Request changes | Request changes |
| 08 Nonroot config access broken | Request changes | Request changes | Request changes | Request changes |
| 09 Optional package usage uncertain | Comment | Request changes | Request changes | Request changes |
| 10 Equivalent script refactor | Approve | Request changes | Approve | Approve |
| 11 Version-only update | Approve | Approve | Approve | Approve |
| 12 Recipes unavailable, limited local scope | Approve | Approve | Request changes | Approve |

## Main failures

1. **PPA advisory did not prevent the false EOL blocker.** All versions raised an
   EOL blocker for an archive-staged application without evidence of a directly
   pulled application source. The candidate also emitted the intended provenance
   advisory, but separately blocked the release anyway.
   See `candidate/case-01/review.json:6-8,21-23` and
   `ppa/case-01/review.md:9`. This is a policy failure, not merely a scorer issue.

2. **The uncertain package removal was still overblocked.** All versions extended
   the whole-part/service removal rule to removing jq from an existing part.
   The final skill's explicit requirement for concrete affected behavior did not
   stop this: it demanded proof of non-use before approval instead of an advisory.
   See `candidate/case-09/review.md:13-21` and `review.json:6-8`.

3. **Intent was sometimes offered as a waiver for demonstrated runtime breakage.**
   For example, the candidate's permissions finding offers explicit confirmation
   of intentional breakage as an alternative to fixing access.
   See `candidate/case-08/review.json:8`. Confirmation can clear the special
   structural-removal rule; it does not make an unchanged startup contract work.

4. **Date/applicability reasoning remains unreliable.** Baseline case10 and PPA
   case12 falsely reject December 1 relative to October 16. December 1 is 46 days
   away, before the January 16 cap. Numerous other reviews label the EOL gate
   pass rather than n/a for archive applications. The candidate avoided those
   two date-based false verdicts, but retained applicability/reporting mistakes.

## Scorer versus policy failures

The candidate case03 has the correct verdict, blocker and recipe delta, but uses
`"line": null` for a citation (`candidate/case-03/review.json:19-20`). The frozen
scorer rejects the schema and assigns zero to every dimension. Its raw verdict
score is therefore 9/12, whereas actual verdict accuracy is 10/12. The oracle,
scorer and outputs were NOT changed after the run. Raw and inspected metrics are
reported separately rather than silently correcting the run.

Other exact-findings losses include duplicate findings (baseline case08),
non-actionable summary notes placed in findings (baseline case05, candidate
case10), and an out-of-range citation (PPA case02). They are reporting defects,
not missed blockers. Summary losses frequently confuse a trigger commit change
with a recipe version change. Gate mismatches often confuse pass with n/a.

Conversely, automated passing scores do not prove correct prose: baseline case11
earns full credit while describing December 1 as more than three months away.
PPA case08 finds the startup regression but marks its regression gate pass.
Candidate case12 correctly disclaims missing recipe checks, then makes an
unsupported claim that CI will verify all of them. Model output requires review.

## Interpretation and next steps

This is an exploratory single-run result, not statistically established improvement.
It uses one model, synthetic provided evidence, a shared structured-output prompt,
and no live PR/source retrieval. The prompt requests summaries from all variants,
so improved summary scores measure comparison/reporting accuracy, not spontaneous
summary generation caused by the new skill. Execution order was not randomized.

The changes did not introduce an observed missed blocker, and the final variant
had fewer false-blocked cases. However, neither targeted negative control passed:
PPA declaration alone and uncertainty alone still caused request-changes verdicts.
The current wording should not be described as validated against those risks.

A useful next iteration would test a narrowly clarified EOL applicability decision,
and explicitly separate whole-part/service removals from individual-package
uncertainty and proven runtime failures. Repeat unchanged baseline and candidate
runs on the same cases, with held-out variations, before claiming improvement.
No skill edits or additional commits were made as part of this benchmark.

## Artifacts

- `scores.json`: untouched raw PATS scores.
- `benchmark-summary.json`: derived per-version totals and per-case verdicts.
- `<version>/<case>/review.md` and `review.json`: model outputs.
- `<version>/<case>/inputs/`: frozen fixture and skill inputs.
- `<version>/<case>/prompt.md` and `skill-version.json`: reporting prompt and skill identity.
- `<version>/<case>/metadata.json`: execution status, token/cost statistics.
