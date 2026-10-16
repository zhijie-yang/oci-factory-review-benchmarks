# OCI Factory Code Review

**Verdict:** Request changes. The proposed source update introduces an EOL end-of-life date that exceeds the 3-month cap required by policy for upstream-sourced rocks without an accepted support plan.

## Inline Findings

`oci/demo/image.yaml:12` — [blocker] EOL date `2026-12-01` exceeds the maximum allowed span of 3 months from today (2026-10-16). Section 2 (Release policy) mandates that rocks built from directly-pulled upstream sources are capped at today + 3 months unless a support plan has been accepted in `CODEOWNERS`. No such plan is documented. Either shorten the end-of-life date to on or before `2026-12-16`, or link to an accepted support plan to justify the extended commitment. (§2)

## Recipe Notes

The source update from commit `0000000000000000000000000000000000000014` to `0000000000000000000000000000000000000015` refactors the `metadata` part's `override-build` script to introduce a `data_dir` shell variable. Per the supplied evidence, both scripts produce identical output, ownership, permissions, and runtime behavior. No parts or services were added, removed or renamed. The deb-security-manifest part remains correctly configured.

## Gates

**Gates:** eol-cap ❌ · deb-manifest ✅ · recipe-regression ✅ · vuln scan → not assessed locally; verify in CI

---

**Summary of changes:** Commit bump with shell variable refactor in metadata part override-build (semantically equivalent per evidence). No track, base, version, parts, or services changes. EOL policy violation requires remediation.
