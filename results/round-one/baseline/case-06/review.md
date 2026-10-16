# OCI Factory code review

**Verdict:** Request changes. Recipe regression: the proposed commit removes the `tini` package that the unchanged enabled service requires.

## Inline comments

`recipes/after/rockcraft.yaml:19` — `[blocker]` Recipe regression (§3). The `app` part's `stage-packages` removes `tini` at line 20, but the `demo` service command (line 14) still executes `/usr/bin/tini -- /usr/bin/demo serve`. Per the evidence, `tini` is the sole supplier of that executable; the prior filesystem has it, the proposed filesystem does not, and no other part or base layer provides it. The service will fail. Restore the `tini` entry or confirm the command change is intentional in the PR description.

## Gates

**Gates:** one-image ✅ · edge-first n/a · EOL cap ⚠ · track naming ✅ · docs n/a · CVE justification n/a · .trivyignore n/a · deb-manifest ✅ · recipe-regression ❌ · vuln scan → not assessed locally; verify in CI

- **EOL cap ⚠**: The 1.2-24.04 track is established and not new; the edge-only restriction applies only to a suspected regression (§2). While the recipe-regression gate is failed, the EOL cap gate itself is satisfied (end-of-life 2026-12-01 is within 3 months and no new upstream source is involved for the main app).
- **Recipe regression ❌**: Proposed commit removes `tini` from staged packages while the service still requires it; see inline comment.

## Summary

The proposed commit bumps the source reference and removes `tini` from staged packages. This change introduces a recipe regression: the service command remains unchanged but will lack the required `/usr/bin/tini` executable. No other actor supplies it.
