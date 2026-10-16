# OCI Factory Code Review

**Verdict:** Approve. Recipe regression gate passes; security manifest requirement is satisfied; no policy violations detected.

## Review Summary

This diff updates the source commit for the demo-rock upload from `000000000000000000000000000000000000000a` to `000000000000000000000000000000000000000b`. The proposed rockcraft.yaml removes the `build-marker` part (a nil part with no output or dependencies) and otherwise maintains identical content.

## Recipe Comparison

**Changes between prior and proposed recipes:**
- `parts`: Removed `build-marker` (nil plugin, no source/packages/output)
- `services`, `app` part, `deb-security-manifest` part, and all metadata: unchanged

**Comparison status:** Assessed (both snapshots available).

## Gate Assessment

- **EOL cap:** n/a — Application is staged from Ubuntu archive (demo-app deb); not upstream-sourced. Security-manifest part is auxiliary tooling, not the application. EOL cap does not apply.
- **Deb-manifest:** ✅ pass — Rock correctly includes `deb-security-manifest` part sourced from `https://github.com/canonical/rocks-security-manifest`, properly wired per recipe requirements (§3).
- **Recipe-regression:** ✅ pass — `build-marker` removal is intentional per author confirmation and evidence (nil part with no output, no ordering dependencies, no behavioral impact). Not a regression.
- **Vulnerability-scan:** Not assessed locally; verify in CI.

## Inline Findings

None. No blockers or nits.

## Notes

- Edge-first release policy satisfied (existing 1.2-24.04 track, edge risk only).
- Track naming correct (SemVer format `1.2-24.04`).
- No new support plan required (non-upstream-sourced application).
