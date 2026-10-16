Review changes.diff as an OCI Factory LOCAL dry run using
.agents/skills/code-review/SKILL.md. Read context.md and the supplied recipe
snapshots and evidence. Treat the frozen facts as authoritative within this
synthetic exercise, not as claims about actual packages or tests.

Work offline using the supplied files only. Do not fetch source repositories,
run builds, contact GitHub, or post anything. Missing evidence is missing;
do not invent it. Do not edit the input files. Only write review.md and
review.json. Review the fixture, not the benchmark machinery or the skill.

Write the normal human-readable review to review.md, including the skill's
verdict, inline findings and gate assessments. Also write review.json as a
machine-readable representation of that SAME review, with this schema:

```json
{
  "verdict": "Approve | Comment | Request changes",
  "scope": "local",
  "findings": [
    {
      "category": "ppa-provenance | eol-cap | recipe-regression | other",
      "severity": "blocker | nit",
      "message": "Specific concern, affected behavior and requested action",
      "evidence": [{"path": "relative/input/path", "line": 1}]
    }
  ],
  "gates": {
    "eol-cap": "pass | fail | n/a | not-assessed",
    "deb-manifest": "pass | fail | n/a | not-assessed",
    "recipe-regression": "pass | fail | n/a | not-assessed",
    "vulnerability-scan": "pass | fail | n/a | not-assessed"
  },
  "comparison": "assessed | not-assessed",
  "changes": ["parts", "services", "packages", "scripts", "version", "repositories"],
  "summary": "Brief factual recipe delta, or explicit comparison limitation"
}
```

Each pipe-separated value above denotes alternatives, not a literal value.
Use empty findings when there are no concerns. Cite real input lines, not
review output lines. Group findings by concern; do not duplicate a finding.
"changes" contains only categories actually changed BETWEEN THE RECIPES,
not trigger changes: packages includes slices; scripts includes permission
and ownership edits; version includes recipe version and source-tag changes.
An unavailable comparison has no inferred changes. Gate pass means assessed
and satisfied, n/a means the rule does not apply, and not-assessed means
unavailable evidence or an unresolved uncertainty. Keep summary disclosures
separate from actionable findings. Do not guess an expected answer.
