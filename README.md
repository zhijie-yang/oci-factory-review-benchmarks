# OCI Factory review benchmarks

Reproducible, synthetic tests for the code-review skill discussed in
[canonical/oci-factory#1255](https://github.com/canonical/oci-factory/pull/1255).
The benchmark tests reasoning over supplied recipes and evidence, not live PR
retrieval, automatic skill discovery, Rockcraft builds or vulnerability scanning.

## Start here

- [Browse the 16 cases](cases/): complete trigger diffs, recipes, context and evidence.
- [Expected outcomes and rationales](expectations.json).
- [Round-one report](results/round-one/BENCHMARK.md).
- [Round-two report](results/round-two/BENCHMARK.md).
- [Skill snapshots](snapshots/) and [source commit/checksum manifest](snapshots/manifest.json).
- [Review prompt](prompt.md), [fixture generator](fixtures.py), and [scoring code](runner.py).

| Case | Scenario | Expected verdict |
| --- | --- | --- |
| [01](cases/case-01/) | PPA declaration; unknown shipped provenance | Comment |
| [02](cases/case-02/) | Direct application source exceeds EOL cap | Request changes |
| [03](cases/case-03/) | Part removal confirmed only upstream | Request changes |
| [04](cases/case-04/) | Directory change removes unconfirmed service | Request changes |
| [05](cases/case-05/) | Confirmed harmless part removal | Approve |
| [06](cases/case-06/) | Package removal leaves startup executable absent | Request changes |
| [07](cases/case-07/) | Slice removal leaves required library absent | Request changes |
| [08](cases/case-08/) | Permissions prevent nonroot configuration access | Request changes |
| [09](cases/case-09/) | Optional package removal; runtime impact unknown | Comment |
| [10](cases/case-10/) | Equivalent script refactor | Approve |
| [11](cases/case-11/) | Version-only bump with compliant EOL | Approve |
| [12](cases/case-12/) | Recipes unavailable; static trigger checks pass | Locally scoped Approve |
| [13](cases/case-13/) | Intentional removal breaks startup; fix promised later | Request changes |
| [14](cases/case-14/) | Permissions tighten but daemon ownership/access remain | Approve |
| [15](cases/case-15/) | Recipes and provenance explicitly unavailable | Locally scoped Approve |
| [16](cases/case-16/) | Optional yq removal; runtime impact unknown | Comment |

Cases 12 and 15 leave recipe-dependent checks not assessed. The review date is frozen
at 2026-10-16. Cases describe fictional assumptions, not observed real failures.
The expected answers stay on the host; only the case files and selected skill
are mounted into each model's workspace.

Cases 13-16 are supplementary same-family variants added after the two published
rounds, not blind holdouts. They were frozen before local compact-skill testing.
Cases 01-12 and their expected outcomes remain unchanged. The published results
below still cover only those original 12 cases; no results are implied for 13-16.

## Recorded results

| Round / version | Raw aggregate | Inspected correct verdicts | False-blocked cases |
| --- | ---: | ---: | ---: |
| One: original | 65.6% | 9/12 | 3 |
| One: PPA-only | 74.0% | 9/12 | 3 |
| One: previous final | 76.0% | 10/12 | 2 |
| Two: original | 69.8% | 9/12 | 3 |
| Two: PPA-only | 70.8% | 8/12 | 4 |
| Two: previous final | 67.7% | 10/12 | 2 |
| Two: revised | 82.3% | 12/12 | 0 |

Every version detected all six required blocker cases in both rounds. The revised
skill fixed the two targeted false-blocked verdicts in its single run, but still
produced citation, reporting and remediation defects. See the reports rather than
treating verdict agreement as proof of perfect reviews.

The revised wording was tuned using these same cases. **This is an in-sample
regression test, not held-out validation or statistically established improvement.**
All variants share a prompt that requests summaries, so summary scores do not
measure spontaneous summary generation. Execution order was not randomized.

## Reproduce

Requirements: Go 1.26.3 or newer to compile PATS, Python 3.9+ (standard library
only), working Docker, network access, and an OpenRouter key with model access
and credit. No OCI Factory checkout or GitHub authentication is needed.

From this repository root:

```bash
go install github.com/lczyk/pats/cmd/pats@v0.7.2
export PATH="$(go env GOPATH)/bin:$PATH"

# No model calls: checks fixture isolation, scorer behavior and PATS integration.
python3 test_runner.py
pats -c pats.yaml list suites

# Enter the key privately in Bash; do not commit it or put it in pats.yaml.
read -rsp 'OpenRouter API key: ' OPENROUTER_API_KEY
printf '\n'
export OPENROUTER_API_KEY

# Builds the sandbox locally, then runs 64 reviews plus four preflights.
pats -c pats.yaml run -s full -j 4
pats -c pats.yaml score -s full -r 0

# Use the exact .pats/runs/... directory printed by pats run.
python3 runner.py audit .pats/runs/RUN_DIRECTORY
python3 summarize.py .pats/runs/RUN_DIRECTORY
```

If PATS is elsewhere, set `PATS_BIN=/path/to/pats` for the Python tests.
The historical 48-review run cost about $1.31, excluding preflights. The expanded
64-review run would cost roughly $1.75 at that rate; actual costs depend on
provider prices and agent behavior. A single-pair pilot
can use `pats -c pats.yaml run -a revised -t case-01 -j 1`; the full-matrix audit
intentionally rejects partial runs. Model calls send the synthetic inputs to
OpenRouter/provider infrastructure. Network is open inside the sandbox; the
offline-task prompt is not an enforced network restriction. No GitHub token or
working repository is forwarded. The OpenRouter credential is passed to the
container, so use a trusted local Docker daemon and a budget-limited key.

The published configuration rebuilds a local Ubuntu sandbox rather than relying
on the original machine's image ID. OpenCode is pinned to 1.19.3, but the Ubuntu
tag and apt packages are not frozen. Original image IDs and PATS versions remain
in recorded metadata. Model routing can change even with the same model ID.

## Scoring and artifacts

Four dimensions check verdicts, findings, gate assessments and recipe summaries.
Findings require exact category/severity counts and existing input-line citations;
gates receive partial credit; summaries check exact change categories and status.
Malformed JSON/schema or failed executions score zero. The audit rejects missing
cells, since PATS otherwise may average only completed results.

The scorer does not verify semantic citation relevance or Markdown/JSON agreement.
A null citation caused an otherwise correct review to receive zero in both rounds;
reports distinguish raw scores from inspected verdicts. Outputs and scoring policy
were not edited to improve results.

`results/<round>/<version>/<case>/` contains review.md, review.json, metadata.json
and skill-version.json. Common inputs are deduplicated into `cases/`, `snapshots/`
and `prompt.md`; export verified they match every archived run. Report references
to a pair's `inputs/` refer to those shared case files plus its selected snapshot.
Raw event logs, reasoning traces, caches and credentials are deliberately omitted.
Machine-specific run paths in aggregate JSON were replaced with repository-relative
paths; numeric results and individual review artifacts are unchanged. Checksums
of the latter are in [artifact-checksums.json](results/artifact-checksums.json).

Fresh runs are written under ignored `.pats/`, never over the recorded results.
The default configuration and audit now cover round two's four versions across
all 16 cases; recorded 12-case runs are historical artifacts and do not satisfy
the expanded full-matrix audit. See [NOTICE.md](NOTICE.md)
for provenance of the bundled skill snapshots and synthetic content.
