# OCI Factory Review: demo/image.yaml

**Verdict:** Approve. The commit bump introduces a shell-variable refactor in the metadata part with no behavioral impact; all locally-checkable gates pass.

## Inline findings

None.

## Gates

- **EOL cap:** n/a (main application staged from Ubuntu archive, not upstream-sourced)
- **Deb-manifest:** ✅ (deb-security-manifest part present; stage-packages declared)
- **Recipe-regression:** ✅ (shell-variable refactor in override-build, identical output and ownership per evidence)
- **Vulnerability-scan:** → not assessed locally; verify in CI

## Summary

The recipe diff (commit 0000000000000000000000000000000000000015) refactors the `metadata` part's override-build script by introducing a local shell variable `data_dir` to hold the installation path. Per the supplied evidence, both the prior and proposed scripts create identical directory structure (mode 0755), write identical content to `usr/share/demo/name`, and preserve ownership and file modes. Runtime paths are unchanged. The trigger track `1.2-24.04` remains at edge risk and conforms to SemVer naming. No package or service changes are present.
