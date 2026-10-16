# Local review context

This is a wholly synthetic, offline local review, frozen at 2026-10-16.
All names, Git objects, discussions and evidence are fixture assumptions,
not assertions about real Canonical projects or Ubuntu archive contents.
No builds, runtime tests, vulnerability scans or network requests were run.
Review only the supplied material; do not resolve references over the network.

The image demo is already onboarded. The established SemVer track is
1.2-24.04 on Ubuntu 24.04; only its edge risk is targeted. The version
stays within 1.2.x. There are no other track, base or release changes.
There is no accepted support plan or human CODEOWNERS approval of one.
No CVE entries, ignored-vulnerabilities fields or .trivyignore files are
added, removed or modified. Documentation and contacts are unchanged.

## Frozen source index

The source repository for both trigger revisions is canonical/demo-rock.
The following exact repository/commit/path keys identify local snapshots;
the snapshots are the complete recipe text, not excerpts.

| Revision | Commit | Repository path | Local snapshot |
| --- | --- | --- | --- |
| Prior | 0000000000000000000000000000000000000020 | rocks/demo/rockcraft.yaml | recipes/before/rockcraft.yaml |
| Proposed | 0000000000000000000000000000000000000021 | rocks/demo/rockcraft.yaml | recipes/after/rockcraft.yaml |

oci/demo/image.yaml is the proposed trigger. changes.diff is the full
prior-to-proposed trigger diff. The source-index keys, not the synthetic
hash spelling, determine which snapshot is selected.

## Package and source conventions

Unless a recipe's app part has its own source, the main application is
the fictional Ubuntu archive deb demo-app, version 1.2.0, staged by name.
It is not compiled from the trigger repository. The trigger repository
hosts recipes; its organization alone does not identify package provenance.
demo-app and its package/slice metadata are supplied assumptions for this
exercise, not packages to download. Other package names use Ubuntu naming.
No unlisted recipe files, overrides or vulnerability exceptions are implied.
All declared package and slice names resolve in the synthetic package index.
The security-manifest source is an auxiliary build tool, not the main app.

## Supplied discussion

The PR author calls yq an optional convenience tool and requests its removal.
The supplied recipes show no explicit yq invocation, but there is no application
source, runtime inventory, documented tool contract or integration coverage for
optional YAML-processing paths. The author has not supplied usage analysis.
Whether any supported path uses yq cannot be determined from this bundle.
