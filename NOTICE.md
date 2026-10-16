# Provenance

This repository contains synthetic benchmark fixtures and agent-generated reviews
prepared for [canonical/oci-factory#1255](https://github.com/canonical/oci-factory/pull/1255).
It is not an official Canonical benchmark or an independent evaluation.

The skill files under `snapshots/` are verbatim copies from canonical/oci-factory.
Their source commits and SHA-256 checksums are recorded in
`snapshots/manifest.json`; they retain their upstream provenance and are not
relicensed here. No blanket license is asserted for these third-party materials.

[PATS](https://github.com/lczyk/pats/tree/v0.7.2) is an external dependency, not
vendored into this repository. The Dockerfile follows its documented Ubuntu
sandbox pattern but installs only OpenCode, pinned to version 1.19.3.

Review outputs are generated examples, not authoritative maintainer decisions.
Names, package inventories, source references and runtime evidence in the cases
are synthetic. No real builds or security scans were performed for the fixtures.
