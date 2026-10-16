# OCI Factory Code Review

**Verdict:** Approve. The proposed revision updates the application to a patch version (1.2.0 → 1.2.1) without recipe regressions, preserves all existing parts and services, and satisfies all locally-checkable gates.

## Summary

The diff updates `oci/demo/image.yaml` to commit `0000000000000000000000000000000017`, which corresponds to a patch-version application update in the `rockcraft.yaml` recipe. The recipe version field and `app` part's `source-tag` both move from `v1.2.0` to `v1.2.1`. Per context.md, the build/install interface and runtime contract are unchanged; the Makefile and package closure remain stable.

**Recipe delta:**
- `version`: 1.2.0 → 1.2.1
- `app.source-tag`: v1.2.0 → v1.2.1
- All other recipe fields unchanged: services, parts (names, plugin types, build-packages, stage-packages, security-manifest wiring), and run-user are preserved.

## Inline Findings

None.

## Gates Assessment

**EOL cap ✅ pass** – The track `1.2-24.04` has `end-of-life: 2026-12-01`, which is within 3 months of the frozen review date (2026-10-16), satisfying the EOL cap rule. The support plan remains unapproved by a human in `CODEOWNERS`, but no change to end-of-life is proposed; the gate measures the *proposed* state.

**Deb-manifest ✅ pass** – The recipe includes the required security-manifest part (lines 27–32 of both recipes), wired correctly per the documented standard.

**Recipe-regression ✅ pass** – Both the `before` and `after` recipes declare:
- `parts`: `app` and `deb-security-manifest` (no removals)
- `services`: `demo` (no removals)
All script overrides (`demo.override` and `deb-security-manifest.override-prime`) are preserved. The only changes are the version strings and `source-tag`, both reflecting the upstream patch update described in the PR discussion.

**Vulnerability-scan** – Not assessed locally; verify in CI.

---

**Locally-checkable verdict:** ✅ Approve
