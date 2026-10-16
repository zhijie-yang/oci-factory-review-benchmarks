# Code Review: OCI Factory Local Dry Run

**Verdict: Request changes** — The proposed recipe removes the `demo-info` service without confirmed intent from the author.

## Inline Comments

`recipes/after/rockcraft.yaml:11-15` — **[blocker] Recipe regression (§3)** The proposed recipe removes the `demo-info` service that exists in the prior recipe (`rocks/old`). Per §3, when a source bump drops a `services:` entry the previous recipe had, request changes until the removal is restored or the author confirms in the PR that the removal is intentional. An upstream commit message is not confirmation. A discussion comment from the PR author explicitly acknowledging the intentional removal is required before proceeding.

## Gate Assessment

- **EOL cap:** pass — The track's end-of-life date (2026-12-01) is approximately 1.5 months from the review date and within the 3-month maximum allowed.
- **Deb-manifest:** pass — Both recipes correctly include the `deb-security-manifest` part, required because they declare `stage-packages` with deb content.
- **Recipe-regression:** fail — The `demo-info` service was removed without confirmed author intent.
- **Vulnerability-scan:** not-assessed — Not available in local review; verify in CI.

## Summary

The image.yaml diff changes only the recipe directory from `rocks/old` to `rocks/new` at the same commit. Recipe comparison reveals the proposed `rockcraft.yaml` removes the `demo-info` disabled service. The prior recipe's `demo` service and `deb-security-manifest` part remain unchanged. No CVE, vulnerability exception, documentation, or release-policy changes are present. The removal triggers a recipe-regression blocker pending explicit author confirmation of intent.
