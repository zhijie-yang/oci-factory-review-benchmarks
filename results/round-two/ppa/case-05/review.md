# OCI Factory Code Review

**Verdict:** Request changes — EOL cap violation requires a support plan.

## Inline findings

`oci/demo/image.yaml:8` — [blocker] EOL cap violation (§2). The end-of-life date is 2026-12-01, approximately 1.5 months from the review date. The rock is upstream-sourced (via `demo-app` staged from Ubuntu archive), and per §2 Release policy, the EOL cap is at most today + 3 months without an accepted human support plan in `CODEOWNERS`. The context confirms no such plan has been accepted. Request a support plan or move the end-of-life date to within the 3-month window.

## Gates

- **EOL cap**: ❌ fail — EOL date 2026-12-01 exceeds the 3-month cap without an accepted support plan.
- **Deb-manifest**: ✅ pass — The recipe correctly includes `deb-security-manifest` from `canonical/rocks-security-manifest` per §3, wired properly with override-prime.
- **Recipe-regression**: ✅ pass — The `build-marker` nil part was intentionally removed per explicit PR author confirmation; the part has no output or dependencies per supplied evidence, satisfying §3's requirement.
- **Vulnerability-scan**: ➜ not assessed locally — Vulnerability scan is CI-only; cannot assess without running Trivy. Verify in CI.

## Summary

The change is a source bump (commit hash change) in `oci/demo/image.yaml` with a corresponding recipe update removing the `build-marker` nil part. The removal is intentionally confirmed by the author and poses no regression risk. However, the end-of-life date lacks the required support plan authorization under §2 EOL cap rules, triggering a blocker.
