# OCI Factory Code Review

**Verdict:** Request changes. The proposed source commit removes a recipe part without explicit author confirmation, violating the recipe regression rule (§3).

## Inline Findings

`recipes/after/rockcraft.yaml` — [blocker] The `build-marker` part (previously at `recipes/before/rockcraft.yaml:27-28`) is removed in the proposed recipe. Per §3, a source bump that drops a `parts:` entry requires the PR author to explicitly confirm in the PR that the removal is intentional. The frozen upstream commit message ('Intentionally remove the unused build-marker part') does not constitute author confirmation; only a statement from the PR author does. Request the author to confirm this removal is intentional before merging (§3).

## Gates

**eol-cap** ✅ — 2026-12-01 is within the 3-month window from the frozen date 2026-10-16 for an established track under non-upstream-sourced packaging.

**deb-manifest** ✅ — The recipe includes the required security-manifest part sourced from `https://github.com/canonical/rocks-security-manifest` with correct wiring.

**recipe-regression** ❌ — A `parts:` entry (`build-marker`) is dropped in the source bump without explicit PR-author confirmation.

**vulnerability-scan** n/a — not-assessed locally; verify in CI.

## Summary

Source commit bumped from `0000000000000000000000000000000000000006` to `0000000000000000000000000000000000000007`. Recipe diff: removal of the `build-marker` nil part. No other structural changes. Cannot approve pending author confirmation of the intentional part removal.
