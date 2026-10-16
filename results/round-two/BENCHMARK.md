# Round-two skill benchmark

Commit under test: 6f3e7815, `chore: clarify review gates to avoid speculative blockers`.
Date: 2026-10-16. PATS v0.7.2, OpenCode 1.19.3, OpenRouter
anthropic/claude-haiku-4.5. Four concurrent tasks, one execution per case/version.

All 48 tasks exited zero, all four credential preflights passed, and the audit
confirmed 192 score cells. All 96 Markdown/JSON review files were inspected.
The fixtures, oracle, reporting prompt, scoring functions, model and image are
unchanged from round one. Round two adds a fourth frozen skill snapshot and
reruns all three earlier versions. Earlier run artifacts are untouched.

## Results

| Metric | Original 63a27d3b | PPA e996ff5e | Previous final 508d7346 | Revised 6f3e7815 |
| --- | ---: | ---: | ---: | ---: |
| Raw aggregate | 69.8% | 70.8% | 67.7% | 82.3% |
| Inspected matching verdicts | 9/12 | 8/12 | 10/12 | 12/12 |
| Expected blocker cases detected | 6/6 | 6/6 | 6/6 | 6/6 |
| Nonblocking cases falsely blocked | 3/6 | 4/6 | 2/6 | 0/6 |
| Findings scorer | 8/12 | 8/12 | 6/12 | 8/12 |
| Gate scorer | 38/48 | 40/48 | 38/48 | 46/48 |
| Summary scorer | 7/12 | 8/12 | 8/12 | 8/12 |
| Reported task cost | $0.3372 | $0.3183 | $0.3255 | $0.3288 |

Total task cost: $1.3099, excluding credential preflights. Summed task duration
1682.3 seconds is not wall-clock time because tasks ran concurrently. Costs are
harness-reported, not reconciled with an OpenRouter invoice.

Compared with the previous final version in this same round, the revision gains
14.6 percentage points in raw score and two correct verdicts. Its central policy
improvements are visible in both Markdown and JSON, not merely scoring labels.

## Targeted checks

| Case | Expected | Previous final | Revised |
| --- | --- | --- | --- |
| 01 PPA declaration without direct application source | Comment | Request changes | Comment |
| 02 Directly sourced application above EOL cap | Request changes | Request changes | Request changes |
| 03 Unconfirmed whole-part removal | Request changes | Request changes | Request changes |
| 04 Unconfirmed service removal via directory change | Request changes | Request changes | Request changes |
| 05 Confirmed harmless whole-part removal | Approve | Approve | Approve |
| 06 Package removal breaks startup executable | Request changes | Request changes | Request changes |
| 07 Slice removal breaks required plugin library | Request changes | Request changes | Request changes |
| 08 Directory permissions break nonroot config access | Request changes | Request changes | Request changes |
| 09 Optional package removal with uncertain impact | Comment | Request changes | Comment |
| 10 Equivalent shell refactor | Approve | Approve | Approve |
| 11 Version-only bump with compliant EOL | Approve | Approve | Approve |
| 12 Unavailable recipes, limited local approval | Approve | Approve | Approve |

The revised PPA review explicitly says the declaration alone does not trigger
the EOL cap (`revised/case-01/review.md:9`). The uncertain jq removal is a nit,
with runtime safety not assessed (`revised/case-09/review.json:6-8,20`). The
direct-source EOL positive control and all structural/runtime blockers survive.

## Remaining issues

Perfect verdict agreement does not mean fully correct reviews:

- Case12 asserts archive provenance despite unavailable recipes and explicit
  absence of substitute evidence (`revised/case-12/review.md:16`, JSON line6).
  EOL should be not-assessed, not n/a. Its limited local approval remains correct.
- Proven-breakage remedies still sometimes offer intent as an escape condition:
  case08 says corrected "or author intent is confirmed with updated reasoning"
  (`revised/case-08/review.md:20`). Case06 allows intent plus a promise that the
  command will be updated (`revised/case-06/review.md:29`). Neither resolves
  current demonstrated failure. The revised skill explicitly prohibits this;
  compliance is incomplete even though current blockers are correctly reported.
- Case09 says verification is needed "before merge" despite being advisory
  (`revised/case-09/review.md:11`, JSON line8). Its verdict/severity are correct,
  but phrasing still risks turning uncertainty into a merge prerequisite.
- Case03 marks its established part-removal policy violation not-assessed rather
  than fail (`revised/case-03/review.json:24`). No blocker is missed.
- Case01 overstates proposed archive provenance, though it correctly avoids the
  EOL blocker. Unknown PPA package selection is not proof of archive selection.

## Reporting and scorer details

The revised findings scorer failures are case01 (`other` instead of
`ppa-provenance`), case02 (nonexistent trigger line13; actual EOL is line8),
case06 (trigger line14 instead of recipe service-command line14), and case08
(two findings for the same permissions regression). There are seven blocker
entries but only six distinct concerns, all justified; no distinct invented
blocker was found.

Summary failures: case02 adds packages to a version-only delta; case03 calls a
removed part a version change; case08 counts a script edit as a part change;
case12 infers a version change despite unavailable recipes. Several prose
summaries are accurate even when the structured category list is wrong.

The previous-final case03 again uses a null citation line, so the frozen scorer
zeros every dimension. Actual verdict correctness is 10/12 versus the raw
verdict scorer's 9/12. This is reported separately, not silently rescored. No
oracle, score logic or output was changed after model execution.

## Variability and limitations

The original, PPA-only and previous-final raw scores in round one were 65.6%,
74.0%, 76.0%; this round they are 69.8%, 70.8%, 67.7%. Their inspected verdict
counts were 9/12, 9/12, 10/12 and are now 9/12, 8/12, 10/12. This demonstrates
why one aggregate should not be treated as a stable model-performance estimate.
The previous-final PPA and jq failures reproduced in both rounds.

The revised skill has only one run and was tuned using these same 12 cases.
The success is an in-sample regression result, NOT held-out validation or proof
of general reliability. The model, synthetic evidence, explicit structured-output
prompt, nonrandomized execution order and fixed recipe facts limit generalization.
Summary scoring tests requested summaries, not spontaneous skill behavior.

No further skill changes were made in response to this run. The next meaningful
validation would repeat the revised skill on independent provenance/permission/
package-removal variants and other review cases before drawing broad conclusions.

## Artifacts

This directory contains unchanged raw scores.json, derived benchmark-summary.json,
and per-version/case review.md, review.json, metadata.json, inputs/, prompt.md,
and skill-version.json. Skill snapshots and checksums live in the round-two
directory. Repository changes are limited to the committed code-review skill.
