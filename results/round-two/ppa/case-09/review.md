# OCI Factory Local Code Review

**Verdict:** Request changes — Unresolved recipe regression: `jq` removal requires documented confirmation of non-use before release.

## Scope

- **Image:** `oci/demo/image.yaml`
- **Track:** `1.2-24.04` (edge-only, existing)
- **Base:** ubuntu@24.04 (unchanged)
- **Comparison:** Assessed via supplied recipe snapshots

## Inline Findings

`oci/demo/image.yaml:4` — [blocker] Source commit bumped without documented evidence for material recipe change (§3)

`recipes/before/rockcraft.yaml:21` — [blocker] The `jq` package is removed from `app` stage-packages in the new commit. Per §3 recipe-regression, removal of `parts:` or `services:` entries requires explicit author confirmation that the removal is intentional. The context notes no application source, no documented tool contract, and no integration coverage for optional JSON-processing paths. The author's claim that jq is "optional" lacks usage analysis. Whether any supported runtime path depends on jq cannot be determined from this bundle.

**Requested action:** Provide documented evidence (runtime inventory, application source audit, or explicit per-path analysis) that jq is genuinely unused in all supported execution paths, or restore the package. Cite upstream source if applicable.

## Gates

- **EOL cap:** n/a (edge-only existing track, no support plan declared per context)
- **Deb-manifest:** pass (rock includes security-manifest part; no new debs beyond base)
- **Recipe-regression:** fail (package removal unconfirmed)
- **Vulnerability-scan:** not-assessed locally; verify in CI

## Changes

- `packages` (jq removed from stage-packages)

## Summary

Commit `0000000000000000000000000000000000000013` removes `jq` from the `demo-app` rock's build inputs. The trigger and track remain within the established `1.2-24.04` edge-only release. However, the material change to parts composition lacks documented confirmation that removal is safe. Per OCI Factory recipe-regression policy, the author must confirm removal is intentional or restore the package.
