# OCI Factory Local Dry-Run Review

**Verdict:** Request changes

The proposed recipe removes a required package slice, causing a critical runtime regression.

---

## Findings

`recipes/after/rockcraft.yaml:27-30` — **[blocker]** Recipe regression (§3)

The `runtime-libraries` part removes `libgomp1_libs` from staged packages. According to the frozen evidence, the application requires libgomp.so.1 to load its parallel engine; this library is provided exclusively by the removed slice. No other base, remaining package, or part dependency supplies it. The application will fail at startup with an unresolved library error.

The PR author describes this as "reducing staged slices," but per §3, removal of a parts entry requires either restoration or explicit confirmation from the author that the removal is intentional (supported by evidence such as an upstream commit message). A slice reduction without justification is a blocker until resolved. Keep the revision at `edge` (§2) until the regression is addressed.

**Affected line(s):** recipes/after/rockcraft.yaml:27-30 (removal of line 31: `- libgomp1_libs`)

---

## Gates

- **EOL cap:** n/a (support plan not required, version within 1.2.x)
- **Deb manifest:** pass (present and correctly wired)
- **Recipe regression:** ❌ fail (libgomp1_libs removal breaks startup)
- **Vulnerability scan:** → not assessed locally

---

## Summary

A single source commit bump (000e → 000f) modifies the `runtime-libraries` part by removing `libgomp1_libs`. This drop is a blocker recipe regression: the staged application cannot load its required parallel engine without libgomp.so.1, which this slice alone provides in the current rootfs composition.

**Changes between recipes:** packages (slice removal in runtime-libraries)
