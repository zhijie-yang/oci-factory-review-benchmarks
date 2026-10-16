# OCI Factory Code Review

**Verdict:** Request changes. The recipe regression (removal of `demo-info` service without author confirmation) blocks approval per §3.

## Inline Comments

`oci/demo/image.yaml:9` — [blocker] The directory change from `rocks/old` to `rocks/new` corresponds to removal of the `demo-info` service from the recipe (recipes/before/rockcraft.yaml:16-19 vs recipes/after/rockcraft.yaml). §3 requires confirmation from the author that this removal is intentional; the statement "Use the other recipe directory" does not constitute that confirmation. While the service is disabled at startup and has no runtime dependency per evidence.md, the removal must be explicitly acknowledged before proceeding. Request an explicit confirmation (e.g., "Intentional removal of demo-info service") in the PR discussion.

## Gates

- **Deb-manifest:** ✅ — Both recipes include the required security-manifest part (recipes/before/rockcraft.yaml:25-29, recipes/after/rockcraft.yaml:21-25).
- **Recipe-regression:** ❌ — Service `demo-info` is dropped without PR-author confirmation that removal is intentional.
- **EOL cap:** ⚠️ — The track end-of-life is `2026-12-01`, approximately 1.5 months from the review date, well within the 3-month cap, but no support plan is documented per context.md line 12.
- **Edge-first:** n/a — No new track, base or release risk change; existing edge risk is targeted.

## Summary

The diff changes only `upload.directory` from `rocks/old` to `rocks/new`. The corresponding recipe change removes the `demo-info` service. Per §3 (Recipe regression), this removal requires explicit author confirmation that it is intentional before the revision can proceed. Evidence confirms the service is disabled at startup and independent of the primary `demo` service, but the removal is not acknowledged in the supplied discussion.
