# OCI Factory Code Review

**Verdict:** Request changes

The proposed commit and EOL update violate the EOL cap rule (§2). The `demo` app is upstream-sourced from `canonical/demo-rock` (recipe line 19), and no human support plan approval has been recorded in `CODEOWNERS`. The new EOL date 2027-04-16 extends 6 months beyond today (2026-10-16), exceeding the maximum 3-month cap of 2027-01-16. A support plan must be accepted or the EOL must be reduced to 2027-01-16 or earlier.

## Inline findings

- `oci/demo/image.yaml:13` — [blocker] EOL cap exceeded (§2). App part sources from `canonical/demo-rock` (recipe line 19) and is upstream-sourced. No human support plan approval is recorded. New EOL 2027-04-16 exceeds the 3-month cap (today 2026-10-16 → max 2027-01-16). Reduce EOL or provide accepted support plan.

## Recipe comparison

Source-tag patch bump (v1.2.0 → v1.2.1):
- **Version:** 1.2.0 → 1.2.1
- **Parts:** No change (app, deb-security-manifest both present)
- **Services:** No change (demo service unchanged)
- **Packages:** No change (libc6 stage-package unchanged)
- **Scripts:** No change (makefile and override-prime unchanged)

The patch update contains no behavioral or structural changes per supplied evidence.

## Gates

- **EOL cap** ❌ — Exceeds 3-month limit from today without accepted support plan
- **Deb-manifest** ✅ — Present; rock adds stage-packages
- **Recipe-regression** ✅ — No parts or services removed; patch-version bump only
- **Vulnerability-scan** → not assessed locally; verify in CI
