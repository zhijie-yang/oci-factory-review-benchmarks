# Code Review: demo image trigger update

**Verdict:** Request changes. A recipe regression (removed `jq` package) lacks evidence of safe removal.

## Summary of changes

Source commit bump in `oci/demo/image.yaml` from `0000000000000000000000000000000012` to `0000000000000000000000000000000013`. Recipe change: `jq` package removed from app part `stage-packages`.

## Findings

### `oci/demo/image.yaml:8` — [blocker] Recipe regression: jq removal not evidenced (§3)

The source bump removes the `jq` package from `stage-packages` in the app part (recipes/before/rockcraft.yaml:21 → recipes/after/rockcraft.yaml line absent). Per §3, a recipe regression requires either restoration or explicit author confirmation that the removal is intentional.

The context notes the author claims `jq` is optional and requests its removal, but also states: *"there is no application source, runtime inventory, documented tool contract or integration coverage for optional JSON-processing paths. The author has not supplied usage analysis. Whether any supported path uses jq cannot be determined from this bundle."*

This removal cannot be confirmed as safe. Provide:
- Evidence that no supported runtime path invokes jq (grep output from services, app entry point, pebble configuration), or
- Restore the package, or
- Confirm in the PR the removal is intentional with supporting analysis

## Gates

- **EOL cap:** pass — existing track, no new upstream requirement; fixture EOL unchanged.
- **Deb-manifest:** pass — `deb-security-manifest` part present; required and correctly wired.
- **Recipe-regression:** fail — `jq` removal unconfirmed.
- **Track naming:** pass — `1.2-24.04` follows SemVer convention.
- **Edge-first:** pass — edge risk only; no stable or candidate.
- **Vulnerability scan:** not-assessed — local review; CI-only gate.

---

*This is a local dry-run review. All facts are fixture assumptions per context.md.*
