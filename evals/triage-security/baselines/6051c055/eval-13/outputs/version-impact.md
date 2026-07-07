# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | fix present (>= 0.11.14) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | fix present (>= 0.11.14) |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed at Latest Tag? |
|--------|-----------|-----------------|--------------------|-----------------------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |

### Analysis

- **Stream 2.2.x**: The fix is already present in the latest releases (2.2.3 and 2.2.4 ship quinn-proto 0.11.14). The upstream branch `release/0.4.z` already includes the fix. No remediation task is needed for this stream.

- **Stream 2.1.x**: All versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). The upstream branch `release/0.3.z` does NOT have the fix. Remediation is required: an upstream backport to bump quinn-proto on `release/0.3.z`, followed by downstream propagation in `rhtpa-release.0.3.z`.

## Summary

- **Scoped stream (2.2.x)**: Partially affected (2.2.0-2.2.2), but already fixed in 2.2.3+. No remediation task needed.
- **Cross-stream (2.1.x)**: Fully affected (all versions). Remediation required. Since the issue is scoped to 2.2.x and stream 2.1.x has no dedicated CVE Jira, this triggers **Case B** (cross-stream impact with preemptive remediation tasks).
