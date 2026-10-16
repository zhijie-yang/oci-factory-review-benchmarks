# Code Review: OCI Factory Local Dry Run

**Verdict: Request changes**

The proposed directory change introduces an unconfirmed service regression that must be resolved before merging.

## Inline Findings

`oci/demo/image.yaml:5` — **[blocker]** Recipe regression: `demo-info` service removed (§3)

The prior recipe (`rocks/old/rockcraft.yaml`) includes a `demo-info` service (lines 16–19 of `recipes/before/rockcraft.yaml`). The proposed recipe (`rocks/new/rockcraft.yaml`) omits it entirely (lines 12–15 of `recipes/after/rockcraft.yaml`). Per the OCI Factory review standard, removal of a `services:` entry requires explicit PR-author confirmation that the removal is intentional. No such confirmation is present in the supplied discussion.

**Requested action:** Either restore the `demo-info` service in the proposed recipe, or add a comment in the PR confirming that its removal is intentional and explaining the rationale.

## Gates

- **eol-cap:** n/a (no upstream source pull; fictional archive package, not compiled from trigger repository)
- **deb-manifest:** pass (security-manifest part is present; the rock stages `demo-app` from `stage-packages`, not bare-based)
- **recipe-regression:** fail (service removal unconfirmed)
- **vulnerability-scan:** not-assessed (CI-only; static rules still apply)

## Summary

The trigger changes only the `directory` field from `rocks/old` to `rocks/new` at the same commit, routing the build to a different recipe directory within the same revision. Recipe comparison is available and complete. The proposed recipe drops the `demo-info` service without explicit author confirmation, violating §3 regression rules.
