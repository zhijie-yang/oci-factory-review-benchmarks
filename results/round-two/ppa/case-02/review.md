# OCI Factory Code Review

**Verdict:** Request changes — the proposed end-of-life date exceeds the EOL cap and requires a documented support plan or reduction to within 3 months of today.

## Inline findings

`oci/demo/image.yaml:8` — [blocker] EOL cap violation (§2). The application is upstream-sourced (`app` part sources `https://github.com/canonical/demo-rock`). Under §2, without an accepted support plan in `CODEOWNERS`, `end-of-life` must not exceed today (2026-10-16) + 3 months ≈ 2027-01-16. The proposed date 2027-04-16 is 91 days beyond this cap. Either reduce the EOL date to within the cap, or provide a documented support plan for maintainer approval.

## Gates

**Gates:** edge-first n/a · EOL cap ❌ · track naming ✅ · recipe-regression ✅ · deb-manifest ✅ · recipe-regression ✅ · deb-manifest ✅ · recipe comparison ✅ · vuln scan → not assessed locally

- **EOL cap:** ❌ fail — proposed end-of-life 2027-04-16 exceeds maximum allowed date 2027-01-16 for upstream-sourced rocks without a support plan.
- **Track naming:** ✅ pass — `1.2-24.04` follows the correct format (major.minor-base, no patch for SemVer).
- **Recipe regression:** ✅ pass — no parts or services dropped between commit 0000000000000000000000000000000000000004 and 0000000000000000000000000000000000000005.
- **Deb manifest:** ✅ pass — security-manifest part is present in both recipe snapshots.
- **Recipe comparison:** ✅ pass — recipes are available and comparable; source bump is v1.2.0 → v1.2.1 with no structural changes.

## Summary

The trigger updates the recipe commit from `0000000000000000000000000000000000000004` to `0000000000000000000000000000000000000005`, corresponding to a patch-version bump in the upstream application from v1.2.0 to v1.2.1. The end-of-life date is extended from 2026-12-01 to 2027-04-16. Per frozen evidence, the application versions use the same build/install interface with no package, service, script, path or permission changes. The primary blocker is the EOL cap violation. Changes detected: version (upstream application tag).
