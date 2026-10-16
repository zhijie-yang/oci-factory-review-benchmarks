# OCI Factory Code Review

**Verdict:** Request changes.

The proposed commit bump cannot be assessed without the source recipes. §3 recipe review rules require fetching `rockcraft.yaml` at both the prior and proposed commits to detect recipe regressions (dropped parts/services), verify deb-security-manifest compliance, and establish package provenance for §2 EOL cap evaluation. The supplied context explicitly confirms both snapshots are unavailable offline, making the recipe-regression and deb-manifest gates not-assessed.

## Summary

This diff updates a single `upload[]` item's commit hash from `0000000000000000000000000000000000000018` to `0000000000000000000000000000000000000019` in `oci/demo/image.yaml`, targeting the existing stable track `1.2-24.04` at `edge` risk with an end-of-life date of 2026-12-01. The trigger itself is structurally valid and contains no CVE changes, documentation edits, or CI modifications.

## Inline Findings

- `oci/demo/image.yaml:4` — [blocker] Commit bump in upstream-sourced trigger requires recipe comparison. Per §3, a source bump demands fetching the prior and proposed `rockcraft.yaml` to verify no `parts:` or `services:` entries were dropped (recipe regression), confirm deb-security-manifest compliance for any stage-packages, and confirm package source provenance. Both snapshots are missing from this offline review bundle; recipe gates cannot pass.

## Gates

- **edge-first:** ✅ pass — Track and risk exist in prior releases; no new track or base.
- **track-naming:** ✅ pass — Track key `1.2-24.04` matches the SemVer-<base> convention (1.2.x omits patch).
- **EOL-cap:** ⚠ not-assessed — Upstream-sourced image (canonical/demo-rock) with no CODEOWNERS support plan. Per §2, EOL must be ≤ today + 3 months (2026-10-16 + 3mo ≈ 2027-01-16). The trigger declares 2026-12-01, within the cap. However, without the recipe snapshot, package provenance cannot be confirmed; upstream-sourced status is inferred from the repository organization, not verified. A human support plan would eliminate uncertainty.
- **deb-manifest:** ❌ not-assessed — Recipe snapshot unavailable; cannot verify if new stage-packages or deb scripts require `rocks-security-manifest` part.
- **recipe-regression:** ❌ not-assessed — Recipe snapshot unavailable; cannot verify whether prior `parts:` or `services:` entries were dropped.
- **vulnerability-scan:** ⚠ not-assessed — Local review cannot run CI scans; no CVE fields modified in this diff.

## Requested Changes

1. Provide the prior and proposed `rockcraft.yaml` snapshots (at commits `0000000000000000000000000000000000000018` and `0000000000000000000000000000000000000019` from `canonical/demo-rock` / `rocks/demo`) or confirm availability in CI for gate validation.
2. If recipe regression is suspected or a `parts:` / `services:` entry was intentionally removed, confirm the removal in this PR comment so the revision can be held at `edge` per §2 suspected-regression guidance.
3. If the image is upstream-sourced (confirmed by recipe), provide or commit to a human support plan per §2 EOL cap (today + 3 months); the declared EOL aligns but needs human sign-off in CODEOWNERS.

## Notes

- The trigger structure, track naming, and release-risk placement are sound.
- No documentation, CI, CVE, or existing-entry changes detected.
- End-of-life date 2026-12-01 is 46 days from the review date (2026-10-16) and aligns with the 3-month cap if upstream-sourced; confirmation of intent and support plan needed before approval.
