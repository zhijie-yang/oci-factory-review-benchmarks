# OCI Factory Code Review

**Verdict: Request changes** — Recipe regression: the proposed build drops the `demo-info` service without confirmation.

## Inline Findings

### Recipe Regression — BLOCKER (§3)

`oci/demo/image.yaml:9` — [blocker] The recipe change from `rocks/old` to `rocks/new` (at commit 0000000000000000000000000000000000000008) drops the `demo-info` service that was present in the prior recipe. The prior recipe (`recipes/before/rockcraft.yaml:16–19`) includes:

```yaml
demo-info:
  override: replace
  command: /usr/bin/demo --print-version
  startup: disabled
```

The proposed recipe (`recipes/after/rockcraft.yaml`) removes this entry entirely. Per the code-review skill, a source bump that removes a `services:` entry is a recipe regression and requires either restoration or explicit PR-author confirmation that the removal is intentional. The context states: "No PR-author confirmation of the demo-info service removal is present."

**Evidence:**
- `recipes/before/rockcraft.yaml:16–19` (demo-info service definition)
- `recipes/after/rockcraft.yaml` (demo-info service absent)
- `evidence.md:7–8` (demo-info was an on-demand service with no hard dependency on primary)
- `context.md:48` (no confirmation from author)

**Requested action:** Either restore the `demo-info` service in the proposed recipe or confirm in the PR (by explicit comment, not inferred from commit message) that its removal is intentional. Until resolved, do not promote this revision beyond `edge`.

---

## Gate Assessments

**Gates:** deb-manifest ✅ · recipe-regression ❌ · EOL-cap ✅ · track-naming ✅

- **deb-manifest (PASS):** Recipe adds `stage-packages` (demo-app) and includes the required `deb-security-manifest` part, correctly configured per skill guidelines.
- **recipe-regression (FAIL):** Service removed without confirmation; blocker unresolved.
- **EOL-cap (PASS):** End-of-life date `2026-12-01` is within 3 months of baseline `2026-10-16`; main application (demo-app) is deb-only, not upstream-sourced.
- **track-naming (PASS):** Track `1.2-24.04` follows SemVer convention (patch omitted from key).

---

## Summary

The diff narrows the recipe directory reference from `rocks/old` to `rocks/new` within the same commit. The proposed recipe removes the `demo-info` service (an on-demand informational endpoint that calls the same upstream binary as the primary `demo` service with no hard dependency on it). This constitutes a recipe regression under §3 of the code-review skill and requires author confirmation before approval. All other gating rules assessed locally are satisfied.
