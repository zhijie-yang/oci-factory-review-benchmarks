# OCI Factory Code Review – demo/image.yaml

**Verdict:** Request changes. Recipe snapshots are unavailable; deb-manifest and recipe-regression gates cannot be assessed locally.

---

## Inline Findings

`oci/demo/image.yaml:4` — [blocker] Recipe snapshots missing. The frozen index references `canonical/demo-rock` commit `0000000000000000000000000000000000000019` at `rocks/demo/rockcraft.yaml` (proposed snapshot), but `recipes/after/rockcraft.yaml` is not supplied. Similarly, the prior commit `0000000000000000000000000000000000000018` snapshot is not provided. (§3)

Without both snapshots:
- The deb-manifest gate cannot verify whether this source bump adds `.deb` content beyond the base and whether the security-manifest part is present (§3 MUST).
- The recipe-regression gate cannot verify whether any `parts` or `services` entries were dropped in the bump (§3 blocker).

These are mandatory-check prerequisites, not optional context.

---

## Static Gates (Locally Checkable)

- **EOL cap:** ✅ Pass. End-of-life `2026-12-01` is within 3 months from frozen date 2026-10-16, consistent with §2 rules and the absence of an accepted support plan.
- **Edge-first:** ✅ Pass. The 1.2-24.04 track is existing (already onboarded); no new track is introduced.
- **Track naming:** ✅ Pass. The unchanged track key `1.2-24.04` conforms to `<version>-<base>` for SemVer applications (§2).

## Recipe Gates (Unassessed)

- **Deb-manifest:** ❌ Not assessed. Recipe snapshots unavailable.
- **Recipe-regression:** ❌ Not assessed. Recipe snapshots unavailable.
- **Vulnerability scan:** ➜ Not assessed locally. Verify in CI.

---

## Summary

The diff is a source commit bump on an existing track (1.2-24.04, edge-first not required). Static checks (EOL cap, track naming, edge-first) pass. However, the recipe snapshots specified in context.md are not supplied. Without `recipes/before/rockcraft.yaml` and `recipes/after/rockcraft.yaml`, the mandatory deb-manifest and recipe-regression checks cannot proceed. These gates block approval.

Supply both snapshots to resolve the deb-manifest (§3 MUST) and recipe-regression (§3 blocker) checks.
