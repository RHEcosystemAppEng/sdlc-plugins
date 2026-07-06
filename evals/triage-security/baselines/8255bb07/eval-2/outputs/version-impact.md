# Version Impact Analysis -- TC-8002

## CVE-2026-28940: serde_json (affected: versions before 1.0.135, fixed: 1.0.135)

### Stream-Scoped Analysis

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).
Per the triage-security skill, all streams are analyzed for version impact, but
Steps 3-8 actions are scoped to the 2.2.x stream. Cross-stream impact on 2.1.x
is reported via Case B if applicable.

### Version Impact Table

| Version | Stream | Build Tag | serde_json version | Affected? | Notes |
|---------|--------|-----------|-------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | >= 1.0.135 (patched) |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | >= 1.0.135 (patched) |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | >= 1.0.135 (patched) |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | >= 1.0.135 (patched) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | >= 1.0.135 (patched) |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | >= 1.0.135 (patched) |

### Summary

**No supported versions are affected.**

Every version across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.137,
which is above the fix threshold of 1.0.135. The vulnerability (CVE-2026-28940)
only affects serde_json versions before 1.0.135.

- Earliest serde_json version shipped: **1.0.137** (in 2.1.0 and 2.1.1)
- Latest serde_json version shipped: **1.0.139** (in 2.2.3 and 2.2.4)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold by at least 2 patch versions

### Dependency Chain Context

Not applicable -- no versions are affected, so no dependency chain tracing is needed.
The library serde_json is a Cargo (Rust) dependency present in Cargo.lock at all
build tags, but all shipped versions are already patched.

### Upstream Fix Status

Not applicable for remediation purposes since no versions are affected. For
completeness, the upstream branches already carry patched versions:

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Already patched (ships 1.0.137) |
| 2.2.x | Cargo | release/0.4.z | Already patched (ships 1.0.139) |
