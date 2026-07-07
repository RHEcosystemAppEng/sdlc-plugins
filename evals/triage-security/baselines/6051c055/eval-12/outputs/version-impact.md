# Step 2 — Version Impact Analysis

## CVE-2026-48901 (h2 < 0.4.8)

**Enriched fix threshold**: 0.4.8 (from Step 1.5 cross-validation of MITRE CVE API and OSV.dev)

**Issue scope**: Scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`)

All streams are analyzed to detect cross-stream impact. The enriched fix threshold 0.4.8 is used for all comparisons — h2 versions strictly less than 0.4.8 are affected.

## Version Impact Table

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) — scoped stream

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.2 | v0.4.9 | — | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Summary

| Stream | Affected Versions | Not Affected Versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 (all) | — |
| 2.2.x (scoped) | — | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all) |

**Scoped stream (2.2.x)**: No versions are affected. All 2.2.x builds ship h2 >= 0.4.8.

**Cross-stream (2.1.x)**: All versions are affected. Both 2.1.x builds ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (h2 is listed in Cargo.toml dependencies)
  Ecosystem: Cargo
  Profile: production (h2 is a runtime HTTP/2 protocol dependency)

  Stream 2.1.x: h2 0.4.5 (affected) — present in all versions
  Stream 2.2.x: h2 0.4.8+ (not affected) — fixed from first release

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on release/0.3.z branch
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked — mock data does not include branch HEAD) | Unknown |
| 2.2.x | Cargo | release/0.4.z | (not checked — all versions already ship fixed h2) | N/A |

## Triage Outcome

- **Scoped stream 2.2.x**: NOT affected. No versions in the scoped stream ship a vulnerable version of h2. All 2.2.x builds include h2 >= 0.4.8 (the fix version). Recommend closing TC-8030 as **Not a Bug** with VEX justification **Component not Present** (the vulnerable version of h2 is not present in any 2.2.x build).

- **Cross-stream 2.1.x**: AFFECTED. All 2.1.x versions ship h2 0.4.5 (< 0.4.8). This triggers **Case B** (cross-stream impact) — post a cross-stream impact comment on TC-8030 and create preemptive remediation tasks for the 2.1.x stream.
