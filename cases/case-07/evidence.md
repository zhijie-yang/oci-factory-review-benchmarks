# Synthetic evidence

These are definitive assumptions of this fictional fixture, not output
from actual builds, commands or tests. They apply to the exact snapshots
indexed in context.md on 2026-10-16. No runtime test has been executed.

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
