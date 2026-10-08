# Version Impact Analysis — TC-8002

## CVE-2026-28940: serde_json (affected versions before 1.0.135, fixed in 1.0.135)

### Version Impact Table

| Version | Stream | Build Tag | serde_json version | Affected? | Notes |
|---------|--------|-----------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | ships fixed version |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | ships fixed version |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | ships fixed version |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | ships fixed version |
| 2.2.2 | 2.2.x | `v0.4.9` | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | ships fixed version |

### Analysis

**No supported version is affected.** Every version across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.135 (the fix threshold). The earliest shipped version (2.1.0, tag `v0.3.8`) includes serde_json 1.0.137, which is already two patch versions past the fix.

The vulnerable range (serde_json < 1.0.135) was never shipped in any supported product version. The dependency was already at a fixed version before the first supported release was built.

### Scoped Impact (2.2.x stream only — issue scope)

Within the issue's scoped stream (2.2.x):
- 2.2.0: serde_json 1.0.138 — NOT affected
- 2.2.1: serde_json 1.0.138 — NOT affected
- 2.2.2: serde_json 1.0.138 — NOT affected (retag of 2.2.1)
- 2.2.3: serde_json 1.0.139 — NOT affected
- 2.2.4: serde_json 1.0.139 — NOT affected

All versions in the 2.2.x stream ship serde_json well above the fix threshold of 1.0.135.

### Cross-stream Impact (2.1.x stream)

The 2.1.x stream is also NOT affected:
- 2.1.0: serde_json 1.0.137 — NOT affected
- 2.1.1: serde_json 1.0.137 — NOT affected

### Upstream Fix Status

Not applicable — no versions are affected, so upstream fix status is moot. For reference, all upstream branches already ship serde_json versions well above the fix threshold.
