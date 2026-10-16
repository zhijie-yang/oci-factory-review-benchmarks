# OCI Factory Code Review

**Verdict:** Request changes. EOL extension exceeds the 3-month cap without accepted support plan approval.

## Summary

The proposed revision updates `canonical/demo-rock` from commit 0000000000000000000000000000000000000002 to 0000000000000000000000000000000000000003, extending the end-of-life date from 2026-12-01 to 2027-04-16 for the `1.2-24.04` track. The recipe diff adds a PPA declaration (`canonical-demo/stable`) under `package-repositories`. The track remains at `edge` risk only.

## Inline Findings

`oci/demo/image.yaml:8` — [blocker] EOL extension to 2027-04-16 exceeds the 3-month cap (§2 EOL cap). Today is 2026-10-16; maximum allowed end-of-life is 2027-01-16. An accepted support plan must be recorded in CODEOWNERS before this can proceed.

`recipes/after/rockcraft.yaml:27–29` — [nit] PPA declaration added without documentation of its rationale or impact. The prior revision sourced packages from the Ubuntu archive; the proposed revision introduces `canonical-demo/stable` PPA. No apt candidate/origin report is supplied, so it cannot be verified which packages would be selected from the PPA vs. the archive. If the PPA alters package versions, document the reason for the change in the PR.

## Gate Assessment

- **EOL cap:** ❌ fail — End-of-life 2027-04-16 exceeds today + 3 months without human CODEOWNERS approval of a support plan.
- **Deb-manifest:** ✅ pass — Both recipes include `deb-security-manifest` part correctly sourced from `https://github.com/canonical/rocks-security-manifest`.
- **Recipe-regression:** ✅ pass — No parts or services dropped between revisions.
- **Vulnerability-scan:** → not assessed locally; verify in CI.

## Changes Detected

- `version`: commit 0000...0002 → 0000...0003; end-of-life 2026-12-01 → 2027-04-16
- `repositories`: PPA `canonical-demo/stable` added

---

**Local review complete.** The locally-checkable gates are blocked by the EOL cap violation. Resolve before merging.
