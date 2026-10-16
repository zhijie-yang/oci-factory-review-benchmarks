# Code Review: demo image trigger

**Verdict:** Request changes. The proposed commit removes `tini` from staged packages while the service command requires it, causing runtime failure.

## Findings

### Recipe regression: missing dependency in service command

`recipes/after/rockcraft.yaml:21` — [blocker] The `tini` package has been removed from `stage-packages` in the app part, but the service command (unchanged at line 14) still executes `/usr/bin/tini -- /usr/bin/demo serve`. According to the synthetic evidence provided, neither demo-app, base layers, transitive dependencies, nor any other part supplies `tini`. This breaks the service at runtime: Pebble will fail to execute the command. (§3 recipe regression)

**Requested action:** Either restore `tini` to `stage-packages` in the app part, or confirm that the removal is intentional and provide explicit justification in the PR description. If the dependency is no longer needed, the service command must be updated to remove the reference to `/usr/bin/tini`.

## Gates

- **deb-manifest:** pass — A deb-manifest part is present (line 22–26) and correctly configured.
- **recipe-regression:** fail — Staged package `tini` removed without corresponding service command update.
- **eol-cap:** pass — EOL cap is set to 2026-12-01, within 3 months of the frozen date (2026-10-16).
- **vulnerability-scan:** not-assessed — Local review does not perform vulnerability scanning.

## Summary

The trigger diff advances commit `000000000000000000000000000000000000000c` to `000000000000000000000000000000000000000d` within the established 1.2-24.04 track on Ubuntu 24.04. The source recipe removes the `tini` package from staged packages, but does not update the service command that depends on it. This constitutes a recipe regression that will fail at runtime.
