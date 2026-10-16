## OCI Factory Local Code Review

**Verdict:** `Request changes` — The proposed EOL date violates the 3-month cap for upstream-sourced applications without an accepted support plan.

### Inline Findings

`oci/demo/image.yaml:8` — **[blocker]** The end-of-life date `2027-04-16` exceeds the 3-month maximum allowed by §2 (EOL cap). The app part sources directly from `https://github.com/canonical/demo-rock` (recipes/after/rockcraft.yaml:19), making this upstream-sourced. Context confirms no accepted support plan or human CODEOWNERS approval exists. Per §2, "end-of-life is at most today + 3 months." The frozen review date is 2026-10-16; the allowed cap is 2027-01-16. Request: either shorten the EOL to comply, or provide an accepted support plan in CODEOWNERS for review.

### Gates

**Gates:** edge-first n/a · EOL cap ❌ · track naming ✅ · deb-manifest ✅ · recipe-regression ✅ · vulnerability-scan → not assessed locally

- **edge-first:** n/a — Track `1.2-24.04` is established; this is not a new track.
- **EOL cap:** ❌ fail — Upstream-sourced application exceeds 3-month maximum without support plan approval.
- **track naming:** ✅ pass — `1.2-24.04` follows SemVer convention (1.2.x → 1.2-base).
- **deb-manifest:** ✅ pass — Recipe includes required `deb-security-manifest` part with `stage-packages: [libc6]` deb content.
- **recipe-regression:** ✅ pass — Both recipes contain `app` and `deb-security-manifest` parts; `demo` service unchanged. No dropped entries.
- **vulnerability-scan:** not assessed locally; verify in CI.

### Changes Summary

**Comparison:** assessed

**Changed categories:**
- `version`: rockcraft.yaml version `1.2.0` → `1.2.1` (patch bump in source tag)
- `repositories`: trigger commit `0000000000000000000000000000000000000004` → `0000000000000000000000000000000000000005`

**Recipe delta:** Patch-version update from v1.2.0 to v1.2.1 (per evidence.md: same build/install interface, no package/service/script/path/permission changes). EOL extended 6 months to 2027-04-16.
