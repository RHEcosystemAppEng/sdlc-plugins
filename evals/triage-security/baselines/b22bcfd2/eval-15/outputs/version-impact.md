# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from local security-matrix.md files for both configured streams.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: Cargo
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
Affected range: < 0.11.14 (fixed in 0.11.14)

Extracted quinn-proto versions from mock lock file data at each pinned commit tag:

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Pinned Tag | quinn-proto version | Affected? | Notes |
|---------|--------|------------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1, backend tag `v0.4.8`) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Summary**: Versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, and 2.2.2 ship the vulnerable quinn-proto (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)

First appeared: all versions (quinn-proto present in all checked tags)
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Library | Notes |
|--------|-----------|-----------------|---------|-------|
| 2.2.x | Cargo | release/0.4.z | quinn-proto | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.1.x | Cargo | release/0.3.z | quinn-proto | Upstream fix PR: quinn-rs/quinn#2048 |
