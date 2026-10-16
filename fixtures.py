"""Offline, synthetic review inputs; importing this module performs no I/O."""

from difflib import unified_diff
from textwrap import dedent


def _text(value):
    return dedent(value).lstrip("\n")


_HEADER = _text("""
    name: demo
    base: ubuntu@24.04
    build-base: ubuntu@24.04
    version: '1.2.0'
    summary: Demo application
    description: A synthetic application used in an offline review exercise.
    license: Apache-2.0
    platforms:
      amd64:
    run-user: _daemon_
""")

_SERVICE = _text("""
    services:
      demo:
        override: replace
        command: /usr/bin/demo serve
        startup: enabled
""")

_MANIFEST = """  deb-security-manifest:
    plugin: make
    source: https://github.com/canonical/rocks-security-manifest
    source-type: git
    source-branch: main
    override-prime: gen_manifest
"""

_APP = """  app:
    plugin: nil
    stage-packages:
      - demo-app
"""

_BASE = _HEADER + _SERVICE + "parts:\n" + _APP + _MANIFEST

_REPOSITORY = _text("""
    package-repositories:
      - type: apt
        ppa: canonical-demo/stable
""")

_SOURCE_APP = """  app:
    plugin: make
    source: https://github.com/canonical/demo-rock
    source-type: git
    source-tag: v1.2.0
    build-packages:
      - gcc
      - make
    stage-packages:
      - libc6
"""

_SOURCE_RECIPE = _HEADER + _SERVICE + "parts:\n" + _SOURCE_APP + _MANIFEST

_MARKER = """  build-marker:
    plugin: nil
"""

_SECOND_SERVICE = """  demo-info:
    override: replace
    command: /usr/bin/demo --print-version
    startup: disabled
"""

_SLICES = """  runtime-libraries:
    plugin: nil
    stage-packages:
      - libc6_libs
      - libgomp1_libs
"""

_STATE = r"""  runtime-config:
    plugin: nil
    override-build: |
      install -d -m 0750 "$CRAFT_PART_INSTALL/opt/demo"
      printf '%s\n' 'listen=8080' > "$CRAFT_PART_INSTALL/opt/demo/server.conf"
      chmod 0644 "$CRAFT_PART_INSTALL/opt/demo/server.conf"
      chown 584792:584792 "$CRAFT_PART_INSTALL/opt/demo"
"""

_SCRIPT = r"""  metadata:
    plugin: nil
    override-build: |
      install -d -m 0755 "$CRAFT_PART_INSTALL/usr/share/demo"
      printf '%s\n' 'demo' > "$CRAFT_PART_INSTALL/usr/share/demo/name"
"""

_SCRIPT_NEXT = r"""  metadata:
    plugin: nil
    override-build: |
      data_dir="$CRAFT_PART_INSTALL/usr/share/demo"
      install -d -m 0755 "$data_dir"
      printf '%s\n' 'demo' > "$data_dir/name"
"""

def _trigger(commit, directory, eol):
    return _text(f"""
        version: 2
        upload:
          - source: canonical/demo-rock
            commit: '{commit}'
            directory: {directory}
            release:
              1.2-24.04:
                end-of-life: '{eol}'
                risks:
                  - edge
    """)


def _case(number, before, after, *, notes="", evidence=""):
    # Distinct, fixed 40-digit hex identifiers, not claims about real Git objects.
    old_commit = f"{number * 2:040x}"
    new_commit = f"{number * 2 + 1:040x}"
    old_directory = new_directory = "rocks/demo"
    if number == 4:
        new_commit = old_commit
        old_directory, new_directory = "rocks/old", "rocks/new"
    old_eol = "2026-12-01"
    new_eol = "2027-04-16" if number in (1, 2) else old_eol
    old_trigger = _trigger(old_commit, old_directory, old_eol)
    new_trigger = _trigger(new_commit, new_directory, new_eol)
    context = _text(f"""
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
        | Prior | {old_commit} | {old_directory}/rockcraft.yaml | recipes/before/rockcraft.yaml |
        | Proposed | {new_commit} | {new_directory}/rockcraft.yaml | recipes/after/rockcraft.yaml |

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

    """) + notes.strip() + "\n"
    if before is None and after is None:
        context += _text("""

            Neither source-index snapshot is available in this offline bundle.
            The table records the requested lookup keys and intended local paths,
            not successful retrievals. There is no cached recipe, package inventory,
            provenance record or prior review to substitute for either snapshot.
            The package conventions above do not establish this image's contents.
        """)
    files = {
        "oci/demo/image.yaml": new_trigger,
        "changes.diff": "".join(unified_diff(
            old_trigger.splitlines(keepends=True),
            new_trigger.splitlines(keepends=True),
            fromfile="a/oci/demo/image.yaml",
            tofile="b/oci/demo/image.yaml",
            n=len(old_trigger.splitlines()),
        )),
        "context.md": context,
    }
    if before is not None:
        files["recipes/before/rockcraft.yaml"] = before
    if after is not None:
        files["recipes/after/rockcraft.yaml"] = after
    if evidence:
        files["evidence.md"] = _text("""
            # Synthetic evidence

            These are definitive assumptions of this fictional fixture, not output
            from actual builds, commands or tests. They apply to the exact snapshots
            indexed in context.md on 2026-10-16. No runtime test has been executed.

        """) + _text(evidence)
    return files


CASES = {
    "case-01": _case(
        1, _BASE, _BASE + _REPOSITORY,
        notes="""The PR author requests the source revision and EOL updates shown in the diff.
The only recipe edit is the additional PPA declaration. The PPA name is synthetic.
The prior package selection used the Ubuntu archive. No apt candidate/origin
report is supplied for the proposed revision, so the declaration does not tell
which, if any, shipped packages would be selected from the PPA. There is no
main-application source checkout in either recipe.""",
    ),
    "case-02": _case(
        2, _SOURCE_RECIPE,
        _SOURCE_RECIPE.replace("1.2.0", "1.2.1"),
        notes="""The PR author requests the source revision and EOL updates shown in the diff.
Here the app part, not just the trigger, directly checks out canonical/demo-rock.
Its v1.2.0 tag maps to 1111111111111111111111111111111111111111 and v1.2.1
maps to 2222222222222222222222222222222222222222 in the frozen source index.
Those application tags are distinct from the trigger commits selecting recipes.
Both application tags provide a Makefile honoring DESTDIR and installing demo
under /usr/bin. These are frozen synthetic source facts, not online lookups.""",
        evidence="""
            The two app tags use the same build/install interface and runtime
            contract. The source change is a patch-version update without package,
            service, script, path or permission changes. libc6 supplies the dynamic
            runtime; the unchanged Makefile and package closure provide all inputs.
        """,
    ),
    "case-03": _case(
        3, _BASE + _MARKER, _BASE,
        notes="""Frozen upstream commit message: 'Intentionally remove the unused build-marker
part.' The local PR author has only said 'Update the source commit.' There is
no PR-author statement confirming the part removal. No other discussion exists.""",
        evidence="""
            build-marker is a nil part with no source, packages, scripts or output.
            No other part has an ordering dependency on it. Its removal changes
            neither the installed filesystem nor the service execution contract.
        """,
    ),
    "case-04": _case(
        4, _BASE.replace("parts:\n", _SECOND_SERVICE + "parts:\n"), _BASE,
        notes="""The PR changes only upload.directory, from rocks/old to rocks/new, at the
same commit. Both directories exist in that commit and map to the two supplied
snapshots. The author says 'Use the other recipe directory.' No PR-author
confirmation of the demo-info service removal is present.""",
        evidence="""
            demo-info was an on-demand informational service, disabled at startup.
            Its /usr/bin/demo --print-version command uses the same archive binary
            as the primary service. The primary service has no dependency on it.
        """,
    ),
    "case-05": _case(
        5, _BASE + _MARKER, _BASE,
        notes="""Frozen upstream commit message: 'Intentionally remove the unused build-marker
part.' In this PR, the PR author explicitly states: 'I confirm that removing
build-marker is intentional. It is an empty nil part with no outputs or users;
please retain its removal in this source update.'""",
        evidence="""
            build-marker is a nil part with no source, packages, scripts or output.
            No other part has an ordering dependency on it. Its removal changes
            neither the installed filesystem nor the service execution contract.
        """,
    ),
    "case-06": _case(
        6,
        _BASE.replace("command: /usr/bin/demo serve", "command: /usr/bin/tini -- /usr/bin/demo serve")
        .replace("      - demo-app\n", "      - demo-app\n      - tini\n"),
        _BASE.replace("command: /usr/bin/demo serve", "command: /usr/bin/tini -- /usr/bin/demo serve"),
        notes="The PR author describes the source update as reducing staged packages.",
        evidence="""
            For the specified amd64 base and complete resolved package closure,
            tini is the sole supplier of /usr/bin/tini. The prior final filesystem
            contains that executable (root:root, 0755). The proposed final filesystem
            has no /usr/bin/tini, symlink at that path, or alternative tini binary.
            Neither demo-app nor any transitive dependency, base layer, manifest
            output or other part supplies it; no package pulls tini transitively.
            There are no mounts, injected files or later installation steps.
            Pebble executes the unchanged enabled service command literally, with
            no shell fallback.
        """,
    ),
    "case-07": _case(
        7,
        _BASE.replace("command: /usr/bin/demo serve", "command: /usr/bin/demo serve --engine parallel") + _SLICES,
        _BASE.replace("command: /usr/bin/demo serve", "command: /usr/bin/demo serve --engine parallel")
        + _SLICES.replace("      - libgomp1_libs\n", ""),
        notes="The PR author describes the source update as reducing staged slices.",
        evidence="""
            demo-app ships /usr/bin/demo and /usr/lib/demo/parallel.so. The unchanged
            --engine parallel option requires loading parallel.so before listening.
            The plugin ELF DT_NEEDED includes libgomp.so.1. Loading is mandatory for
            this selected engine: an unresolved library causes startup to exit.
            The app deb does not depend on libgomp1 because this engine is optional
            at package level; the recipe supplies its library explicitly by slice.
            In this frozen slice index, libc6_libs does not depend on libgomp1_libs.
            The libgomp1_libs slice supplies the only libgomp.so.1 symlink and target
            in the prior complete rootfs. After removing it, neither the base,
            remaining slice closure, full deb dependency closure, manifest tool nor
            any other part supplies libgomp.so.1 or its target, in any directory.
            libc and the ELF interpreter remain present in both snapshots. There
            is no alternate loader search path, cached usable copy, preload, mount,
            fallback engine or runtime installation.
        """,
    ),
    "case-08": _case(
        8,
        _BASE.replace("command: /usr/bin/demo serve", "command: /usr/bin/demo serve --config /opt/demo/server.conf") + _STATE,
        _BASE.replace("command: /usr/bin/demo serve", "command: /usr/bin/demo serve --config /opt/demo/server.conf")
        + _STATE.replace("0750", "0700").replace("584792:584792", "0:0"),
        notes="The PR author describes the source update as adjusting configuration directory permissions.",
        evidence="""
            In the frozen Rockcraft user mapping, _daemon_ has UID and GID 584792.
            The unchanged run-user selects that identity for the demo service.
            The runtime has no DAC override/search capability, ACL grant, root
            helper or identity-changing step. Staging preserves the override-build
            directory ownership and modes. No other part overwrites /opt/demo.
            Before: /opt/demo is 584792:584792 mode 0750. After: it is 0:0 mode 0700.
            /opt and all ancestors are searchable; server.conf remains 0:0 mode
            0644 with identical contents. The configured app must open this file
            before listening, with no fallback.
            No volume or later permission change modifies these paths.
        """,
    ),
    "case-09": _case(
        9, _BASE.replace("      - demo-app\n", "      - demo-app\n      - jq\n"), _BASE,
        notes="""The PR author calls jq an optional convenience tool and requests its removal.
The supplied recipes show no explicit jq invocation, but there is no application
source, runtime inventory, documented tool contract or integration coverage for
optional JSON-processing paths. The author has not supplied usage analysis.
Whether any supported path uses jq cannot be determined from this bundle.""",
    ),
    "case-10": _case(
        10, _BASE + _SCRIPT, _BASE + _SCRIPT_NEXT,
        notes="The PR author requests the source update containing the shell-variable refactor.",
        evidence="""
            Both override-build bodies execute in the same shell environment with
            the same CRAFT_PART_INSTALL and umask. data_dir is an ordinary unset,
            non-readonly shell variable and the override shell is private to this
            part. Both scripts create the same directory with mode 0755 and write
            identical content ('demo' followed by a newline) to usr/share/demo/name,
            with identical ownership and file mode. No additional commands or
            consumers of the temporary variable exist. Runtime paths are unchanged.
        """,
    ),
    "case-11": _case(
        11, _SOURCE_RECIPE, _SOURCE_RECIPE.replace("1.2.0", "1.2.1"),
        notes="""The PR updates only the recipe version and the main app's source-tag to 1.2.1.
Here the app is built directly from canonical/demo-rock. In the frozen source
index v1.2.0 maps to 1111111111111111111111111111111111111111 and v1.2.1
maps to 2222222222222222222222222222222222222222. These application refs
are separate from the trigger commits selecting the supplied recipe snapshots.
Both tags have a Makefile honoring DESTDIR and installing demo under /usr/bin.
There is no request to extend the trigger's existing 2026-12-01 EOL.""",
        evidence="""
            The two app tags use the same build/install interface and runtime
            contract. The source change is a patch-version update without package,
            service, script, path or permission changes. libc6 supplies the dynamic
            runtime; the unchanged Makefile and package closure provide all inputs.
        """,
    ),
    "case-12": _case(
        12, None, None,
        notes="The PR author requests the source commit update. Neither recipe was supplied.",
    ),
}
