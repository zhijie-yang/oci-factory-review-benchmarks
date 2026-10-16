# Code Review: demo image trigger update

**Verdict:** Request changes. The proposed recipe drops a mandatory runtime dependency, causing application startup failure.

## Inline findings

`changes.diff:7-8` — `recipes/after/rockcraft.yaml:29` — [blocker] Recipe regression: the `runtime-libraries` part removed `libgomp1_libs` from `stage-packages`. The service command `/usr/bin/demo serve --engine parallel` loads `parallel.so`, which requires `libgomp.so.1` as a mandatory `DT_NEEDED` dependency (evidence.md:8-12). Removing this slice leaves no other source for the library (base, remaining slices, and full deb closure do not provide it). The application will exit at startup. Restore `libgomp1_libs` or confirm the removal is intentional and documented in the PR description (§3).

## Gates

- **EOL cap:** ✅ pass — `end-of-life: 2026-12-01` is ~46 days from 2026-10-16, under the 3-month cap.
- **Deb-manifest:** ✅ pass — `deb-security-manifest` part is present and correctly configured (§3).
- **Recipe-regression:** ❌ fail — `libgomp1_libs` slice removed without documented justification; required library becomes unavailable at runtime.
- **Vulnerability-scan:** n/a — not assessed locally; verify in CI.

## Summary

Trigger commit changed from `000000000000000000000000000000000000000e` to `000000000000000000000000000000000000000f`. Recipe comparison shows one packages change: `libgomp1_libs` slice removed from the `runtime-libraries` part. No parts, services, scripts, version, or repository changes. EOL cap and track naming rules pass. Deb security manifest correctly present.
