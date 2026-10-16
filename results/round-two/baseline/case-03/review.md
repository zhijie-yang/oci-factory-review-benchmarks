# OCI Factory Local Dry-Run Review

**Verdict:** `Request changes` — Recipe regression: part removal requires explicit author confirmation.

---

## Inline Findings

`oci/demo/image.yaml:8` — [blocker] Recipe regression: the source bump (commit 0000000000000000000000000000000000000007) drops the `build-marker` part that was present in the prior recipe (0000000000000000000000000000000000000006). Per §3, a part removal in a source bump must be confirmed by the PR author in the PR discussion; an upstream commit message alone does not constitute that confirmation. The frozen PR context records only "Update the source commit" from the author, with no statement confirming the intentional removal. Request the author to explicitly confirm in the PR that the `build-marker` part removal is intentional. (§3)

---

## Gates

**Gates:** deb-manifest ✅ · recipe-regression ❌ · EOL cap ✅ · track-naming ✅

- **deb-manifest:** ✅ pass — Recipe adds deb content (demo-app); deb-security-manifest part is correctly wired per documentation.
- **recipe-regression:** ❌ fail — Sourced recipe drops a parts entry without explicit author confirmation in this PR.
- **EOL cap:** ✅ pass — Established edge-only track (1.2-24.04) within acceptable window; no new base or direct upstream source introduction.
- **track-naming:** ✅ pass — No track changes.

---

## Summary

The trigger diff updates a single commit hash in `oci/demo/image.yaml`. The sourced recipe removes the `build-marker` part. Evidence confirms the part is unused (nil, no dependencies, no filesystem impact), and the upstream commit message documents intentional removal. However, the PR author has not explicitly confirmed this removal in the PR discussion. The skill requires explicit author confirmation in the PR to proceed; an upstream message does not substitute for it. Request changes until the author confirms.

**Changes identified:** version (commit hash only, not recipe version or source-tag).
