# Version Impact Analysis -- TC-8002

## CVE-2026-28940: serde_json (versions before 1.0.135)

Fix threshold: **1.0.135**

### Version Impact Table

All supported versions across both streams were analyzed using the pinned source commits from the security matrix.

| Version | Stream | Tag | serde_json version | Affected? | Notes |
|---------|--------|-----|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | ships fixed version (1.0.137 >= 1.0.135) |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | ships fixed version (1.0.137 >= 1.0.135) |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1: 1.0.138) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | ships fixed version (1.0.139 >= 1.0.135) |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | ships fixed version (1.0.139 >= 1.0.135) |

### Summary

**No supported versions are affected.** Every version across both streams ships serde_json at version 1.0.137 or later, which is above the fix threshold of 1.0.135. The vulnerability was already patched in all shipped builds before this CVE was filed.

### Stream-Scoped View (2.2.x -- this issue's scope)

Since TC-8002 is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix, the primary assessment covers:

| Version | serde_json version | Affected? |
|---------|--------------------|-----------|
| 2.2.0 | 1.0.138 | NO |
| 2.2.1 | 1.0.138 | NO |
| 2.2.2 | -- | NO (retag of 2.2.1) |
| 2.2.3 | 1.0.139 | NO |
| 2.2.4 | 1.0.139 | NO |

All versions in the 2.2.x stream ship serde_json >= 1.0.135. None are affected.

### Cross-Stream View (2.1.x -- outside this issue's scope)

The 2.1.x stream is also not affected (serde_json 1.0.137 in all versions), so no cross-stream impact comment is needed.

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | All shipped versions already contain the fix; upstream branch status is moot |
| 2.1.x | Cargo | release/0.3.z | All shipped versions already contain the fix; upstream branch status is moot |

Since no versions are affected, upstream fix status is informational only. No remediation is required.
