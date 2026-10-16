# Synthetic evidence

These are definitive assumptions of this fictional fixture, not output
from actual builds, commands or tests. They apply to the exact snapshots
indexed in context.md on 2026-10-16. No runtime test has been executed.

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
