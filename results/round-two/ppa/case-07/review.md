# Review: demo image trigger update

**Verdict:** Request changes. The proposed revision removes a mandatory runtime dependency, causing the application to fail at startup.

## Inline findings

`recipes/after/rockcraft.yaml:30` — [blocker] recipe regression (§3): The proposed revision removes `libgomp1_libs` from `runtime-libraries` stage-packages, but the service command still uses `--engine parallel` (line 14). According to the supplied evidence, libgomp.so.1 is required for this engine, and `libgomp1_libs` is the only source of this library in the rootfs. Removing it will cause the application to fail at startup with an unresolved library error.

**Requested action:** Restore `libgomp1_libs` to stage-packages, or confirm in the PR that removal is intentional and that an alternative mechanism supplies libgomp.so.1 (the evidence supplied indicates no such alternative exists).

## Gates

- **deb-manifest**: ✅ pass — The recipe includes the security-manifest part as required.
- **recipe-regression**: ❌ fail — A runtime dependency required by the service command was removed without evidence of intentional replacement or deprecation.
- **eol-cap**: ✅ pass — The EOL date (2026-12-01) is within 3 months of the frozen review date (2026-10-16).
- **vulnerability-scan**: → not assessed locally; verify in CI.

## Summary

The trigger commits a source bump from `000000000000000000000000000000000000000e` to `000000000000000000000000000000000000000f` in canonical/demo-rock. The proposed recipe removes the `libgomp1_libs` package slice. The supplied evidence confirms this slice is the sole provider of libgomp.so.1, a mandatory runtime dependency for the configured service engine (parallel). No alternative source or intentional deprecation is documented. The revision should remain at `edge` until this regression is resolved.
