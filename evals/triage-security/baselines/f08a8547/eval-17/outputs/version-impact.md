# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.11.12) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Fix Threshold

- **Vulnerable range**: quinn-proto versions before 0.11.14
- **Fixed version**: 0.11.14
- Versions shipping quinn-proto < 0.11.14 are **affected**
- Versions shipping quinn-proto >= 0.11.14 are **not affected**

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions |
|--------|-------------------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Cross-Stream Impact

The issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`), but the version impact analysis reveals that stream **2.1.x** is also affected:

- **2.1.x**: all versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the affected range

This cross-stream impact triggers **Case A** (proactive remediation) for the 2.1.x stream, unless a sibling CVE Jira already exists for that stream.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.2.x | Cargo | release/0.4.z | YES | v0.4.11+ already ships 0.11.14 |
| 2.1.x | Cargo | release/0.3.z | Needs verification | upstream branch must be checked |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
Upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048
```
