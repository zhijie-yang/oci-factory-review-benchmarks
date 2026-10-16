# OCI Factory Code Review

**Verdict:** Request changes — Recipe package slice removal breaks runtime behavior.

## Summary

The diff updates the trigger commit from `000000000000000000000000000000000000000e` to `000000000000000000000000000000000000000f` for the demo image track `1.2-24.04` (edge). The source recipe removes the `libgomp1_libs` slice from the `runtime-libraries` part's `stage-packages`. This change breaks the image: the demo service is configured to run with `--engine parallel` (recipes/before/rockcraft.yaml:14), which requires the libgomp.so.1 library provided only by the removed slice. No other part or base supplies this library.

## Inline Findings

`recipes/after/rockcraft.yaml:29–30` — **[blocker]** Recipe regression (§3): Package slice `libgomp1_libs` removed from `runtime-libraries` part. The service `demo` at recipes/after/rockcraft.yaml:14 runs with `--engine parallel`, which requires libgomp.so.1 (evidence.md). After removal, libgomp.so.1 is not supplied by any remaining slice, base, or part (evidence.md), and startup will fail. Restore the slice or confirm the engine option is no longer used.

## Gates

**deb-manifest** ✅ — Correctly includes canonical/rocks-security-manifest part (recipes/after/rockcraft.yaml:21–26).

**eol-cap** n/a — Main application demo-app is staged from Ubuntu archive (context.md:33–34), not compiled from a directly-pulled upstream repository; EOL cap does not apply.

**recipe-regression** ❌ — Package slice removal (libgomp1_libs) breaks service startup (evidence.md).

**vulnerability-scan** — not-assessed locally; verify in CI.
