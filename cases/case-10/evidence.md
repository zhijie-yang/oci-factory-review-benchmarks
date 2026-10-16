# Synthetic evidence

These are definitive assumptions of this fictional fixture, not output
from actual builds, commands or tests. They apply to the exact snapshots
indexed in context.md on 2026-10-16. No runtime test has been executed.

Both override-build bodies execute in the same shell environment with
the same CRAFT_PART_INSTALL and umask. data_dir is an ordinary unset,
non-readonly shell variable and the override shell is private to this
part. Both scripts create the same directory with mode 0755 and write
identical content ('demo' followed by a newline) to usr/share/demo/name,
with identical ownership and file mode. No additional commands or
consumers of the temporary variable exist. Runtime paths are unchanged.
