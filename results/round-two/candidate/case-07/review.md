# Code Review: OCI Factory Local Dry Run

**Verdict:** Request changes. The proposed revision removes a critical runtime dependency without maintaining it through alternate means, causing application startup failure.

## Inline Findings

`recipes/after/rockcraft.yaml:27-30` — [blocker] The `runtime-libraries` part removes the `libgomp1_libs` slice present in the prior recipe (line 31 in before). Evidence confirms this causes a runtime failure (§3 recipe regression):
- The `demo` service uses `--engine parallel` (before:14), which requires the `libgomp.so.1` library
- The application ELF binary depends on libgomp.so.1 via DT_NEEDED (evidence.md:8-10)
- The `demo-app` deb package does not declare libgomp1 as a dependency; the recipe must provide it via slice (evidence.md:11-12)
- After removal, no other base, slice, part, or deb dependency supplies this library (evidence.md:15-17)
- This causes the startup command to fail immediately with an unresolved library error (evidence.md:10)

Restore the `libgomp1_libs` slice to the `runtime-libraries` part, or provide an equivalent source for `libgomp.so.1` before this revision is released.

`oci/demo/image.yaml:4` — [nit] No support plan is documented for the track's EOL date (2026-12-01). Per §2 EOL cap guidance, upstream-sourced applications require a support plan in `CODEOWNERS` when EOL exceeds today + 3 months. The recipe does not declare external `package-repositories`, so package provenance is deb-only; however, this is close to the boundary. Consider documenting the maintenance expectation in the PR description or `CODEOWNERS` entry (advisory note, not blocking).

## Gates

**one-image** ✅ · **edge-first** ✅ · **EOL cap** ⚠ (no documented support plan; within 3-month window) · **track naming** ✅ · **docs** n/a · **CVE justification** n/a · **deb-manifest** ✅ · **recipe-regression** ❌ (libgomp1_libs removed; startup fails) · **vuln scan** → not assessed locally; verify in CI

## Summary

The proposed commit removes the `libgomp1_libs` slice from the `runtime-libraries` part. The prior recipe staged this slice to supply libgomp.so.1, which is required by the application binary when the `--engine parallel` option is used (the active service command). The evidence confirms that without this library, the application fails at startup and cannot recover via base, remaining slices, deb dependencies, or any other part. This is a concrete recipe regression that breaks the core service behavior and must be resolved before release.
