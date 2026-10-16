# OCI Factory Code Review

**Verdict:** Request changes — The proposed EOL date exceeds the 3-month cap for upstream-sourced rocks without an accepted support plan.

## Inline Comments

`oci/demo/image.yaml:13` — [blocker] EOL cap violation (§2). The demo rock is upstream-sourced (`parts.app.source` points to `canonical/demo-rock` with `source-type: git`). Without an accepted support plan documented in `CODEOWNERS`, the `end-of-life` date must not exceed today + 3 months. The proposed date `2027-04-16` is approximately 6 months from today (2026-10-16). Per §2, ask for a support plan or reduce the EOL to within 3 months (no later than `2027-01-16`).

## Gates

- **EOL cap** ❌ — Proposed EOL exceeds the 3-month cap without an accepted support plan.
- **Deb-manifest** ✅ — Deb-security-manifest part is present in both recipes.
- **Recipe-regression** ✅ — No parts or services dropped; patch version bump is intentional and documented in source-tag.
- **Vulnerability-scan** — Not assessed locally; verify in CI.

## Changes

- `version` (recipe version and source-tag: `1.2.0` → `1.2.1`)
- `end-of-life` date (extension from `2026-12-01` to `2027-04-16`)

## Summary

The proposed trigger revision advances the demo rock from v1.2.0 to v1.2.1, a patch-version bump with no recipe changes (same parts, services, build packages, and runtime contract). The deb-security-manifest part is present and properly configured. However, the end-of-life date extension violates the 3-month cap for upstream-sourced rocks. Either provide an accepted support plan or amend the EOL to within 3 months.
