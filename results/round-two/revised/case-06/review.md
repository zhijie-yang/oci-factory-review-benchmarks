# Review: demo image (oci/demo/image.yaml)

**Verdict:** Request changes

The source recipe change removes the `tini` package, but the service command still requires `/usr/bin/tini`. This is an evidenced runtime regression that blocks approval.

## Inline findings

`recipes/after/rockcraft.yaml:20` — **[blocker]** The package `tini` has been removed from `stage-packages`, but the service command in `oci/demo/image.yaml:14` still references `/usr/bin/tini -- /usr/bin/demo serve` unchanged. According to evidence.md:8–12, the proposed final filesystem contains no `/usr/bin/tini` executable or symlink, and no other source supplies it. The service will fail to start. (§3)

**Proposed fix:** Either restore `tini` to stage-packages in the recipe, or update the service command to use `/usr/bin/demo serve` directly (if that is the intended runtime behavior). Confirm the fix with the author.

## Recipe change summary

The commit bump (000c → 000d) involves a single package change:

- **Packages removed:** `tini`
- **Packages retained:** `demo-app`, manifest part, and all parts/services unchanged

## Gates

- **EOL cap:** n/a — demo-app is staged from the Ubuntu archive (not upstream-sourced from a directly-pulled external repository)
- **Deb-manifest:** pass — security-manifest part present and correctly wired
- **Recipe-regression:** fail — evidenced removal of `/usr/bin/tini` while service command still depends on it
- **Vulnerability-scan:** not-assessed (local review; verified in CI)

## Assessment notes

This is a local dry-run review. The vulnerability-scan gate is CI-only and remains unassessed. The recipe-regression gate fails on evidence; the change cannot proceed to approval. Keep the revision at edge (§2) until the removal is resolved or the author confirms in the PR that the breakage is intentional and the service command will be updated.
