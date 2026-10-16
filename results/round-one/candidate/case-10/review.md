# Review: OCI Factory Local Dry Run

**Verdict:** Approve. All locally-checkable gates pass; the commit bump contains only a cosmetic shell-variable refactor with no behavioral change.

## Summary

The diff updates `oci/demo/image.yaml` to commit `0000000000000000000000000000000000000015`, whose recipe refactors the metadata part's override-build script to use a shell variable for readability, without altering output or runtime behavior.

## Gates

- **EOL cap:** ✅ pass. End-of-life 2026-12-01 is ~46 days away, within the 3-month cap. The app (demo-app, staged by name) is not upstream-sourced; no support plan applies.
- **Deb-manifest:** ✅ pass. The security-manifest part is correctly present and wired; the app part stages demo-app (a deb package) requiring the manifest.
- **Recipe-regression:** ✅ pass. No parts or services removed; the override-build refactor is equivalent per evidence.
- **Vulnerability scan:** → not assessed locally; verify in CI.

## Inline findings

`recipes/after/rockcraft.yaml:29-32` — [nit] The override-build script has been refactored to use a shell variable `data_dir` for improved readability. Per evidence.md, both the prior and proposed scripts produce identical directory creation (mode 0755), file content ('demo\n'), ownership, and file mode. No behavioral change detected.

## Changes detected

- version: commit only (source bump within 1.2.x, no recipe version change)
- scripts: override-build refactored (no behavioral change per evidence)
