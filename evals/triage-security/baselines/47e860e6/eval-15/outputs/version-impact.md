# Step 2 – Version Impact Analysis

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | retag of 2.2.1 (same as 2.2.1; lock file check skipped) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version shipped |

Evidence: simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output from the mock matrix data.

## Summary

- In-scope stream 2.2.x: affected versions **2.2.0, 2.2.1, 2.2.2**; 2.2.3 and 2.2.4 are not affected (ship 0.11.14).
- Out-of-scope stream 2.1.x: **2.1.0, 2.1.1 affected**. Handled by Case A (cross-stream impact).
- Development stream (Step 2.2): no unreleased Jira version or branch-HEAD data in the inputs, so it could not be evaluated. Needs confirmation before closing out the analysis.

## Dependency chain (Step 2.3.5)

quinn-proto is a transitive dependency of the backend (typically `quinn` -> `quinn-proto`, pulled in via the HTTP/3/QUIC stack). Remediation: bump the direct dependency first, and if that doesn't work, pin quinn-proto >= 0.11.14 via `cargo update -p quinn-proto`. Runtime dependency (not dev-only).

## Upstream fix status (Step 2.5)

- 2.2.x (`release/0.4.z`): tags v0.4.11/v0.4.12 already ship 0.11.14, so the upstream branch very likely contains the fix. Branch HEAD was not inspected in this eval. If confirmed, the remediation task is a **dependency bump / release rebuild** rather than a backport.
- 2.1.x (`release/0.3.z`): no evidence of a fix (latest tag v0.3.12 ships 0.11.9). An upstream backport is needed.
