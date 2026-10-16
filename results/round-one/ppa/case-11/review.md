# OCI Factory Local Review

**Verdict:** Approve. All locally-checkable gates pass; recipe patch bump within the established track is clean and safe to release to edge.

---

## Gate Results

- **EOL cap:** ✅ pass — 2026-12-01 remains within the 3-month cap (context.md frozen at 2026-10-16).
- **Deb-manifest:** ✅ pass — `deb-security-manifest` part present in both recipes (recipes/before/rockcraft.yaml:27–32, recipes/after/rockcraft.yaml:27–32).
- **Recipe-regression:** ✅ pass — No parts or services dropped; `deb-security-manifest` and `app` preserved in identical structure.
- **Vulnerability-scan:** not-assessed — Local review; no CI run executed.

---

## Findings

No blockers or nits found.

---

## Comparison

**Assessed.** Both recipe snapshots supplied; prior and proposed recipes compared.

**Recipe delta:**
- `version`: 1.2.0 → 1.2.1 (recipes/before:4, recipes/after:4)
- `app.source-tag`: v1.2.0 → v1.2.1 (recipes/before:21, recipes/after:21)
- All other fields unchanged

**Trigger delta** (changes.diff):
- `commit`: 0000...16 → 0000...17 (change.diff:7–8)

**Release configuration:** Unchanged (1.2-24.04 track, edge risk, 2026-12-01 EOL).

---

## Summary

The proposed revision updates the recipe and trigger commit to reflect a patch-level version bump (1.2.0 → 1.2.1) of the demo-rock application. The source repository (`canonical/demo-rock`) remains unchanged; only the tag moves from v1.2.0 to v1.2.1. Per evidence.md, both tags use the same build interface and runtime contract with no package, service, script or permission changes. The security-manifest part is retained. The track is established and the EOL policy is satisfied. No recipe regression, deb-manifest violation or early promotion violation detected.
