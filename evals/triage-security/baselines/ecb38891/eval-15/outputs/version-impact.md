# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. Matrix Last-Updated: 2026-06-28T10:00:00Z (within the 14-day threshold -- staleness check passed silently).

Issue is scoped to **2.2.x stream**, but all streams are checked per Important Rule 4 (check ALL supported versions) to support Case A cross-stream impact detection.

## 2.3 -- Dependency Version Extraction

Using pinned commit tags from the supportability matrix (not branch HEAD) per Important Rule 13.

### 2.2.x Stream (in-scope)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### 2.1.x Stream (cross-stream check for Case A)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |

## Version Impact Summary

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | cross-stream (2.1.x) |
| 2.1.1 | 0.11.9 | YES | cross-stream (2.1.x) |
| 2.2.0 | 0.11.9 | YES | in-scope |
| 2.2.1 | 0.11.12 | YES | in-scope |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed |
| 2.2.4 | 0.11.14 | NO | fixed |

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.1.x | Cargo | release/0.3.z | Cross-stream -- requires separate check |
