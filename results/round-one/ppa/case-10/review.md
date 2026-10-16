# OCI Factory Local Review: demo

**Verdict:** Approve. The source commit bump introduces a semantically-equivalent shell-variable refactor with no recipe regression, and all locally-checkable gates pass.

## Summary

The proposed changes bump `oci/demo/image.yaml` from commit `...014` to `...015` within the established 1.2-24.04 track on Ubuntu 24.04 (edge risk only). The rockcraft.yaml recipe is structurally identical; the sole functional change is in the `metadata` part's `override-build` script, which refactors an inline path into a shell variable `data_dir` before use. Per the supplied evidence, both scripts produce identical filesystem state, permissions, and content.

## Inline Findings

- `oci/demo/image.yaml:4` — Recipe includes required `deb-security-manifest` part (§3 MUST), correctly sourced from `https://github.com/canonical/rocks-security-manifest` and wired per documentation. The rock stages `demo-app` from deb, so the manifest is required. ✓
- `recipes/before/rockcraft.yaml` → `recipes/after/rockcraft.yaml` — No parts or services dropped; metadata refactor is internal only. ✓

## Gates

- **eol-cap** n/a — The application is not upstream-sourced; it is staged from the Ubuntu archive as `demo-app` per convention.
- **deb-manifest** ✅ pass — Security manifest present and correctly configured.
- **recipe-regression** ✅ pass — All parts and services retained; refactor is equivalent.
- **vulnerability-scan** → not assessed locally; verify in CI.

## Local Approval Scope

This local review confirms that the trigger change and its sourced recipe satisfy §1–§3 checks accessible offline: no recipe regression, required security manifest in place, and no vulnerability fields modified. Promotion to `stable` or concurrent track changes, if any, remain out of scope for this single-image, single-risk local run.
