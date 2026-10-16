# Code Review: demo image trigger update

**Verdict:** Approve. The source bump is a pure refactoring that maintains identical build behavior and passes all locally-checkable gates.

## Summary

`oci/demo/image.yaml` bumps the commit from `0000000000000000000000000000000000000014` to `0000000000000000000000000000000000000015`. The corresponding recipe change refactors the `metadata` part's `override-build` script to use a `data_dir` shell variable. Per the supplied evidence, both versions produce identical directory structure, content, ownership and permissions. No parts or services are dropped. The image remains at `edge` on track `1.2-24.04` with EOL 2026-12-01, well within the 3-month cap.

## Recipe changes (§3)

`recipes/after/rockcraft.yaml` vs `recipes/before/rockcraft.yaml`:

- `metadata.override-build`: Lines 29–31 introduce a `data_dir` shell variable (line 30) and refactor two subsequent lines (31–32) to use it instead of inline paths. The evidence confirms identical output: directory mode 0755, file content 'demo' with newline, and identical ownership and file mode.
- No parts added, removed or modified structurally.
- `deb-security-manifest` part is present and correctly wired (required for deb content). ✅

## Gates

- **deb-manifest:** ✅ pass — required part present
- **recipe-regression:** ✅ pass — no parts or services dropped
- **eol-cap:** ✅ pass — 46 days from 2026-10-16 to end-of-life 2026-12-01, within 3-month cap
- **vulnerability-scan:** → not assessed locally; verify in CI

**Merge ready.**
