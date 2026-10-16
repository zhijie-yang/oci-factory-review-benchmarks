# OCI Factory Code Review

**Verdict:** Request changes — source bump removes a recipe part without explicit author confirmation of intentional removal.

## Inline Comments

`oci/demo/image.yaml:8` — [blocker] Commit bump to 0000000000000000000000000000000000000007 removes the `build-marker` part from rockcraft.yaml (compare before lines 27–28 vs. after: absent). Per §3, a source bump that drops a `parts:` entry requires either restoration or author confirmation in the PR that the removal is intentional. The upstream commit message documents the intent, but the PR author's statement is only "Update the source commit" with no separate confirmation. Keep this revision at `edge` pending clarification. (§3 Recipe regression)

## Gates

- **eol-cap** n/a — application is not upstream-sourced; demo-app is staged by name from the Ubuntu archive, not compiled from canonical/demo-rock
- **deb-manifest** ✅ — required; present and correctly configured (canonical/rocks-security-manifest, main branch, gen_manifest override)
- **recipe-regression** ❌ — blocker; `build-marker` part removed without author confirmation
- **vulnerability-scan** → not-assessed locally; verify in CI

## Recipe Comparison

**Changes detected:** parts (build-marker removed)

**Prior recipe (commit 0000000000000000000000000000000000000006):**
- Parts: app, deb-security-manifest, build-marker
- Services: demo (enabled)

**Proposed recipe (commit 0000000000000000000000000000000000000007):**
- Parts: app, deb-security-manifest
- Services: demo (enabled)

**Summary:** The proposed revision removes the `build-marker` nil part (which has no source, packages, or scripts). Per synthetic evidence, its removal changes neither filesystem nor service contract. However, the removal is a recipe regression that triggers the blocker rule absent explicit author confirmation in the PR.
