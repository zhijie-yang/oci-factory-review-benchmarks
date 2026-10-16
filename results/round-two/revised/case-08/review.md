# OCI Factory Code Review

**Verdict:** Request changes. The proposed recipe introduces a runtime regression that prevents the configured service from accessing its required configuration file.

## Inline Findings

`recipes/after/rockcraft.yaml:30` — [blocker] The `/opt/demo` directory is changed from owner `584792:584792 mode 0750` to `0:0 mode 0700`. The `_daemon_` run-user (UID/GID 584792) can no longer read this directory (mode 0700 denies group/other access, and the directory is now owned by root). The service command at `recipes/after/rockcraft.yaml:14` requires access to `/opt/demo/server.conf` before listening, with no fallback or capability override available at runtime. This breaks the application. Restore the previous ownership or establish root-read-capable permissions that preserve service functionality. (§3 recipe-regression)

`recipes/after/rockcraft.yaml:33` — [blocker] Ownership is changed from `chown 584792:584792` to `chown 0:0`. Combined with the mode change on line 30, the non-root run-user loses access to the directory and its contents. Confirm in the PR that this change is intentional, document the new permission model, and verify that the service functions under the new ownership. (§3 recipe-regression)

## Gates

**EOL cap:** n/a (demo-app is from Ubuntu archive, not directly-pulled upstream)  
**Deb-manifest:** pass (security-manifest part present)  
**Recipe-regression:** fail (service cannot access configuration directory under proposed permissions)  
**Vulnerability-scan:** not-assessed (local review, CI-only)  

## Summary

Commit 0000000000000000000000000000000000000011 changes the `/opt/demo` directory ownership and mode in the build-time override script. The directory is reduced from `584792:584792 0750` to `0:0 0700`, preventing the non-root `_daemon_` run-user from reading the directory and accessing `server.conf`. The application requires this file at startup with no fallback, making the change a runtime regression. Hold at `edge` until the permission model is corrected or author intent is confirmed with updated reasoning in the PR.
