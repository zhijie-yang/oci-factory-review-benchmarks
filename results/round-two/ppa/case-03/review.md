# Code Review: OCI Factory Local Dry Run

**Verdict:** Request changes — The proposed source commit removes a recipe part without explicit PR author confirmation of intent.

## Inline Comments

`recipes/after/rockcraft.yaml:16-26` — [blocker] Recipe regression: the `build-marker` part present in the prior recipe (recipes/before/rockcraft.yaml:27-28) has been removed in this source bump. Per §3, removal of a `parts:` entry requires confirmation from the PR author that the removal is intentional; an upstream commit message does not satisfy this requirement. The frozen evidence indicates the removal is operationally harmless (no filesystem impact, no service ordering dependency), but the procedural gate still applies. Request that the PR author explicitly confirm the intentional removal or restore the part. (§3 recipe regression)

## Gates

**Gates:** edge-first ✅ · EOL cap ✅ · track naming ✅ · deb-manifest ✅ · recipe-regression ❌ · vuln scan → not assessed locally

- **edge-first:** ✅ Track 1.2-24.04 is already established; this targets edge risk only.
- **EOL cap:** ✅ End-of-life is 2026-12-01, ~1.5 months from the frozen date (2026-10-16), within the 3-month cap. Main application is from Ubuntu archive (not upstream-sourced).
- **track naming:** ✅ No new or modified track keys; 1.2-24.04 follows SemVer convention.
- **deb-manifest:** ✅ Rock stages demo-app (deb package) and includes properly configured `deb-security-manifest` part per §3 requirement.
- **recipe-regression:** ❌ Source bump removes `build-marker` part without PR author confirmation of intentional removal. The evidence confirms operational safety (nil part, no dependencies, no output), but §3 procedural requirement stands.
- **vuln scan:** not assessed locally (CI-only).

## Summary

The proposed trigger bumps the source commit from `0000000000000000000000000000000000000006` to `0000000000000000000000000000000000000007`, corresponding to a recipe change that removes the `build-marker` part. The upstream commit justifies this as intentional ('Intentionally remove the unused build-marker part'), but the PR author has not explicitly confirmed the removal in this local review context. All other gates pass.
