# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### In-scope stream: 2.2.x

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Summary (2.2.x):** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and
2.2.4 ship the fixed version (0.11.14).

### Cross-stream: 2.1.x (outside issue scope)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |

**Summary (2.1.x):** All 2.1.x versions are affected. This cross-stream impact will be
reported via Case A in Step 8.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

The upstream fix is available on `release/0.4.z` but not on `release/0.3.z`.
Remediation for the 2.2.x stream can pick up the fix from the upstream branch.
The 2.1.x stream requires an upstream backport to `release/0.3.z`.
