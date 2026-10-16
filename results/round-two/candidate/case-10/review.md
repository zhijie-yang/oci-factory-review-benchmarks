# Code Review: demo image.yaml update

**Verdict:** Approve — shell-variable refactor with no functional regression; all locally-checkable gates pass.

## Scope

Single trigger update: `oci/demo/image.yaml` — commit bump from 0000000000000000000000000000000000000014 to 0000000000000000000000000000000000000015 in `canonical/demo-rock` at `rocks/demo`. Review checklist §1–§3 applies.

## Recipe Comparison

**Prior recipe (00000014):** Direct path expansion in override-build
```yaml
override-build: |
  install -d -m 0755 "$CRAFT_PART_INSTALL/usr/share/demo"
  printf '%s\n' 'demo' > "$CRAFT_PART_INSTALL/usr/share/demo/name"
```

**Proposed recipe (00000015):** Shell-variable refactor
```yaml
override-build: |
  data_dir="$CRAFT_PART_INSTALL/usr/share/demo"
  install -d -m 0755 "$data_dir"
  printf '%s\n' 'demo' > "$data_dir/name"
```

**Changes:** scripts (override-build refactoring only); no parts, services, packages, slices, or runtime behavior change.

**Evidence of equivalence:** Both scripts execute in the same environment, create the same directory with mode 0755, write identical content (demo + newline) to usr/share/demo/name with identical ownership and file mode. `data_dir` is a local shell variable, unset initially, private to the part (evidence.md).

## Inline Findings

None — no blockers or nits identified.

## Gate Assessments

- **deb-manifest:** ✅ Pass — `deb-security-manifest` part correctly sourced from `https://github.com/canonical/rocks-security-manifest` at `main` branch with `override-prime: gen_manifest` (recipes/before:21–26, recipes/after:21–26). Required because recipe includes `stage-packages` (app part stages demo-app).

- **recipe-regression:** ✅ Pass — No parts or services removed; override-build refactor is benign, functionally equivalent per evidence; no new runtime regressions.

- **eol-cap:** ✅ Pass — Base is Ubuntu 24.04 (LTS). Application is staged from Ubuntu archive deb (demo-app), not upstream-sourced. No human CODEOWNERS support plan approval required (context.md). End-of-life 2026-12-01 is within 3 months of fixture date (2026-10-16) and tracks to existing edge-only release.

- **vulnerability-scan:** ⚠️ Not assessed locally — network and CI execution required; verify in CI.

**Summary:** All §1–§3 static checks pass. Edge-only release (existing track, no regression) satisfies §2 policy.

---

**Local dry-run complete.** Vulnerability scan and CI gates remain pending.
