# Code Review: OCI Factory LOCAL dry run

**Verdict: Request changes** — The proposed source commit removes a `parts:` entry without author confirmation of intentional removal.

## Findings

### Recipe-regression blocker: part removal lacks author confirmation (§3)

`oci/demo/image.yaml:4` — [blocker] The source commit bump from `0000000000000000000000000000000000000006` to `0000000000000000000000000000000000000007` drops the `build-marker` part from the recipe (removed from `recipes/before/rockcraft.yaml:27-28`). Per §3, a source bump that removes a `parts:` or `services:` entry requires confirmation in the PR that the removal is intentional. The author's statement "Update the source commit" does not provide this confirmation.

The frozen upstream commit message ("Intentionally remove the unused build-marker part") is an upstream artifact, not a PR-author confirmation. Until the author explicitly confirms in the PR discussion that this removal is intentional, the revision must remain at `edge` (§2) and this finding blocks approval.

## Gates

- **eol-cap:** n/a — The main application (demo-app) is staged from the Ubuntu archive, not upstream-sourced.
- **deb-manifest:** pass — The recipe includes the required `deb-security-manifest` part per §3.
- **recipe-regression:** not-assessed — The part removal is evident and evidence shows it is behavior-preserving, but without author confirmation per §3 this gate cannot pass.
- **vulnerability-scan:** not-assessed — Vulnerability scan is CI-only; not performed in local review.

## Summary

The trigger file changes only the source commit hash from `0000000000000000000000000000000000000006` to `0000000000000000000000000000000000000007`. The proposed recipe removes the `build-marker` part, a nil part with no dependencies or runtime impact. However, the part removal lacks the required PR-author confirmation per the code-review skill §3.
