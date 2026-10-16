# OCI Factory Code Review

**Verdict:** Request changes — Part removal requires explicit author confirmation before promoting beyond edge.

## Findings

`oci/demo/image.yaml:4` — [blocker] Recipe regression: `build-marker` part removed (§3)

The proposed commit `0000000000000000000000000000000000000007` removes the `build-marker` part from the recipe. While the frozen upstream commit message states the removal is intentional, **the PR author has not confirmed this in the PR discussion** (per context.md:46). Per §3, a source bump that drops a `parts:` entry requires either restoration or explicit author confirmation—an upstream commit message does not suffice.

The evidence provided confirms `build-marker` is a nil part with no dependencies and its removal has no impact on the filesystem or service execution. However, the procedural requirement for author confirmation remains unmet.

**Requested action:** Reply in the PR confirming that the removal of `build-marker` is intentional and expected, or restore the part in the recipe.

---

## Gates

- **EOL cap:** ✅ pass — Application staged from Ubuntu archive (demo-app), `end-of-life: '2026-12-01'` is within 3 months of today (2026-10-16).
- **Deb-manifest:** ✅ pass — Recipe stages deb packages and includes `deb-security-manifest` part as required.
- **Recipe-regression:** ❌ fail — Part removal lacks author confirmation; cannot promote beyond edge.
- **Vulnerability-scan:** ➡️ not-assessed locally — CI scan required before merge.

---

## Changes

- `parts`: `build-marker` removed

## Summary

Single-file trigger bump to commit `0000000000000000000000000000000000000007` removes the `build-marker` part from the recipe. The part is confirmed to be unused and its removal has no runtime impact. Author confirmation of intentionality is required before the revision can be promoted beyond edge.
