# Synthetic evidence

These are definitive assumptions of this fictional fixture, not output
from actual builds, commands or tests. They apply to the exact snapshots
indexed in context.md on 2026-10-16. No runtime test has been executed.

For the specified amd64 base and complete resolved package closure,
tini is the sole supplier of /usr/bin/tini. The prior final filesystem
contains that executable (root:root, 0755). The proposed final filesystem
has no /usr/bin/tini, symlink at that path, or alternative tini binary.
Neither demo-app nor any transitive dependency, base layer, manifest
output or other part supplies it; no package pulls tini transitively.
There are no mounts, injected files or later installation steps.
Pebble executes the unchanged enabled service command literally, with
no shell fallback.
