# Code Review: OCI Factory LOCAL Dry Run

**Verdict:** Request changes — EOL extension exceeds policy cap; package repository provenance unclear.

## Inline Comments

`changes.diff:13` — [blocker] EOL cap violation (§2). The proposed end-of-life date (2027-04-16) is 6 months from the frozen review date (2026-10-16), exceeding the "today + 3 months" policy limit for upstream-sourced applications. No accepted support plan or CODEOWNERS approval is documented in context. Request a support plan or reduce the EOL date to 2027-01-16 or earlier.

`recipes/after/rockcraft.yaml:27-29` — [nit] Package repository declaration without provenance clarity (§3). The recipe adds a `package-repositories` PPA entry. Per §3 advisory guidance, this potentially marks the rock as upstream-sourced. Context confirms no apt candidate/origin report is supplied, so the proposal does not establish which, if any, shipped packages would come from `canonical-demo/stable` vs. the Ubuntu archive. Confirm the intended package sources in the PR discussion; if packages do ship from the PPA, the EOL cap blocker above applies.

## Gates

- **one-image:** ✅ Single `oci/demo/` trigger touched.
- **edge-first:** ✅ Existing track (1.2-24.04) with no new tracks; edge risk only.
- **EOL cap:** ❌ Proposed date exceeds policy.
- **track-naming:** ✅ Existing track `1.2-24.04` follows SemVer convention.
- **deb-manifest:** ✅ Recipe includes required `deb-security-manifest` part.
- **recipe-regression:** ✅ No parts or services removed; parts and services unchanged.
- **vulnerability scan:** → not assessed locally; verify in CI.

## Summary

The change updates the source commit and extends the EOL window by 6 months. A `package-repositories` PPA is added to the recipe. The proposed EOL (2027-04-16) violates the 3-month policy cap without an accepted support plan. The PPA declaration is an advisory flag requiring clarification on package provenance in PR discussion, but the EOL violation is the blocking issue.
