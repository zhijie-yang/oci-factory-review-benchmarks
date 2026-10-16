# OCI Factory Code Review

**Verdict:** Request changes — The proposed end-of-life date exceeds the §2 EOL cap without an accepted support plan.

## Inline Comments

`oci/demo/image.yaml:13` — [blocker] Proposed end-of-life (2027-04-16) exceeds the EOL cap cutoff (2027-01-16) by 3 months (§2). The app part sources from `https://github.com/canonical/demo-rock` with `source-tag: v1.2.1` (recipes/after/rockcraft.yaml:21), making this an upstream-sourced application. Per the release policy, without an accepted support plan approved by a human listed in `CODEOWNERS`, `end-of-life` must not exceed today + 3 calendar months. Revise the EOL date to 2027-01-16 or earlier, or request human acceptance of a support plan in `CODEOWNERS`.

## Recipe Change Summary

Source bump from trigger commit 0000000000000000000000000000000000000004 to 0000000000000000000000000000000000000005, with app tag update from v1.2.0 to v1.2.1:

- **Version:** 1.2.0 → 1.2.1 (patch bump within SemVer track 1.2-24.04)
- **Parts:** Identical; no removals or additions
- **Services:** Identical; no changes to `demo` service
- **Packages:** stage-packages and build-packages unchanged
- **Scripts:** No changes to override-* scripts or permission/ownership modifications

Per evidence.md, the patch version update uses the same build/install interface and runtime contract with no behavioral changes.

## Gates

- **eol-cap:** ❌ fail — end-of-life 2027-04-16 exceeds cap cutoff 2027-01-16 without accepted support plan
- **deb-manifest:** ✅ pass — `deb-security-manifest` part correctly wired per §3 requirements
- **recipe-regression:** ✅ pass — Patch bump with no behavioral changes; no part/service removals or concerning script/package edits
- **vulnerability-scan:** → not assessed locally; verify in CI

**Comparison:** assessed
