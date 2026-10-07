# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

All quinn-proto versions below 0.11.14 are within the affected range.
Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version.

## Upstream fix status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | NOT FIXED -- latest tags (v0.3.8, v0.3.12) ship quinn-proto 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | FIXED -- latest tags (v0.4.11, v0.4.12) ship quinn-proto 0.11.14 |

## Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock at all inspected tags)
  Profile: production (quinn-proto is a runtime QUIC transport dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.lock
```

## Summary

- **2.1.x stream**: both versions (2.1.0, 2.1.1) affected. Upstream branch release/0.3.z does NOT have the fix.
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected. Versions 2.2.3, 2.2.4 already ship the fix. Upstream branch release/0.4.z already has the fix.
