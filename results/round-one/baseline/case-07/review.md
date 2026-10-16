# OCI Factory Code Review

**Verdict:** Request changes — Recipe regression: removal of `libgomp1_libs` slice will cause the demo service to fail at startup due to missing required library.

## Inline findings

`recipes/after/rockcraft.yaml:30` — [blocker] Recipe regression (§3): the `libgomp1_libs` slice has been removed from `runtime-libraries` stage-packages. Evidence (evidence.md:7–20) establishes that demo-app's parallel engine requires libgomp.so.1, which is only supplied by this slice in the prior rootfs. Removing it without alternative provision will cause the service command (`/usr/bin/demo serve --engine parallel`) to fail with an unresolved library error at startup. The removal must be restored or the author must confirm in the PR that the service configuration has changed to avoid loading this engine. Per §2, while this regression remains unresolved, the revision must stay at `edge` only.

## Gates

**Gates:** EOL cap n/a · deb-manifest ✅ · recipe-regression ❌ · vulnerability-scan → not assessed locally

- **EOL cap:** n/a — The context notes that end-of-life stays within today + 3 months (2026-12-01 is 46 days from fixture date 2026-10-16) and no new support plan is added.
- **deb-manifest:** pass — The recipe includes the `deb-security-manifest` part (recipes/after/rockcraft.yaml:21–26) sourced from the canonical repository as documented in §3.
- **recipe-regression:** fail — A required package slice (`libgomp1_libs`) has been removed from stage-packages without evidence that the service no longer needs it.
- **vulnerability-scan:** not-assessed locally — CI run required; static rules apply.

## Summary

The diff updates the commit hash in `oci/demo/image.yaml` (000000000000000000000000000000000000000e → 000000000000000000000000000000000000000f). The corresponding source recipe change removes the `libgomp1_libs` slice from `runtime-libraries` stage-packages. Evidence confirms this slice is the sole provider of libgomp.so.1 in the prior rootfs, and the service startup command depends on it. No alternative source or configuration change is documented. This constitutes a recipe regression per §3 and blocks approval.
