# Code Review: OCI Factory LOCAL Dry Run

**Verdict:** `Request changes` — EOL cap violation: end-of-life exceeds 3-month ceiling by 3 months without accepted support plan.

---

## Inline Findings

`oci/demo/image.yaml:13` — [blocker] **EOL cap exceeded (§2)**
The upstream-sourced app (`canonical/demo-rock`, app part with external `source:`) is released to edge with `end-of-life: '2027-04-16'`, which is 6 months from the frozen review date (2026-10-16). §2 EOL cap requires at most today + 3 months for upstream-sourced applications without an accepted support plan. Context confirms no `CODEOWNERS` approval exists. Submit a support plan for human review and acceptance before release, or reduce the EOL to 2027-01-16 or earlier.

---

## Recipe Change Summary

The diff updates the trigger commit (0000000000000000000000000000000000000004 → 0000000000000000000000000000000000000005) and EOL, reflecting a source bump. Recipe comparison:

| Aspect | Prior (v1.2.0) | Proposed (v1.2.1) | Change |
| --- | --- | --- | --- |
| **Recipe version** | 1.2.0 | 1.2.1 | patch bump |
| **App source-tag** | v1.2.0 | v1.2.1 | patch bump |
| **App plugin/build** | make, gcc+make, libc6 | make, gcc+make, libc6 | none |
| **Services** | demo (serve) | demo (serve) | none |
| **Parts** | app, deb-security-manifest | app, deb-security-manifest | none |

Evidence confirms: "patch-version update without package, service, script, path or permission changes." The change is version-only and introduces no regressions.

---

## Gates

- **edge-first:** ✅ n/a (no new track)
- **EOL cap:** ❌ fail (exceeds 3-month ceiling without support plan)
- **deb-manifest:** ✅ pass (included and properly configured)
- **recipe-regression:** ✅ pass (no dropped parts/services; patch-only)
- **vuln scan:** → not assessed locally; verify in CI

---

## Summary

Recipe patch from v1.2.0 to v1.2.1 with no structural changes; EOL violation blocks release until support plan is accepted or date is capped at 3 months.
