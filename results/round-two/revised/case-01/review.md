# OCI Factory Code Review

**Verdict:** Comment. The proposed revision updates the trigger commit and extends EOL with no blockers; a PPA addition warrants clarification on package provenance.

## Inline Comments

`changes.diff:7-8` — [nit] Trigger commit updated from `0000000000000000000000000000000000000002` to `0000000000000000000000000000000000000003`. Recipe change (below) must be assessed for regressions. (§3)

`recipes/after/rockcraft.yaml:27-29` — [nit] Additional package repository declared via PPA `canonical-demo/stable`. Per §3 guidance, please clarify which shipped packages, if any, are sourced from this repository. The declaration alone does not establish provenance and does not trigger the §2 EOL cap. (§3)

`changes.diff:12-13` — EOL extended from `2026-12-01` to `2027-04-16` (6 months). Since demo-app is staged from the Ubuntu archive (not directly pulled upstream), the §2 EOL cap is not applicable. (§2)

## Recipe Change Summary

**Between commits `0000000000000000000000000000000000000002` and `0000000000000000000000000000000000000003`:**

- **Parts:** No changes to `parts:` structure or stage-packages. `app` and `deb-security-manifest` remain identical.
- **Services:** No changes. `demo` service unchanged.
- **Packages/slices:** No changes to declared packages; `demo-app` remains the only stage package.
- **Scripts:** No override scripts added or modified.
- **Repositories:** Added `package-repositories` with a single PPA entry. No evidence supplied of which, if any, shipped packages originate from this PPA.
- **Version & source-tag:** Recipe version remains `1.2.0`; source commit bumped per trigger.

## Gates

- **eol-cap:** n/a (application staged from Ubuntu archive, not upstream-sourced)
- **deb-manifest:** pass (correctly configured and unchanged)
- **recipe-regression:** pass (no parts, services, or problematic package removals; PPA addition is advisory only)
- **vulnerability-scan:** not-assessed (local dry run; no CVE entries modified)

## Notes

All assertions (package names, versions, repository structure, freezing date 2026-10-16) are treated as fixture facts per context.md, not real projects. The review is offline and does not fetch source repositories, run builds, or contact GitHub.
