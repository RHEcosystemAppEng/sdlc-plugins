# Affects Versions Correction — TC-8004

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

## Version Impact Evidence

Based on lock file analysis of h2 dependency versions at each pinned source commit:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** (< 0.4.8) |
| RHTPA 2.1.1 | 0.4.5 | **YES** (< 0.4.8) |
| RHTPA 2.2.0 | 0.4.8 | **NO** (>= 0.4.8, ships fixed version) |
| RHTPA 2.2.1 | 0.4.8 | **NO** |
| RHTPA 2.2.2 | -- | **NO** (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | **NO** |
| RHTPA 2.2.4 | 0.4.9 | **NO** |

## Required Corrections

### Versions to ADD

| Version | Reason |
|---------|--------|
| **RHTPA 2.1.1** | Ships h2 0.4.5 (affected) but was missing from PSIRT's Affects Versions |

### Versions to REMOVE

| Version | Reason |
|---------|--------|
| **RHTPA 2.2.0** | Ships h2 0.4.8 (the fixed version) -- not actually affected |

## Corrected Affects Versions

After correction, the Affects Versions field should contain only the versions that actually ship a vulnerable h2 version:

- **RHTPA 2.1.0** (h2 0.4.5 -- affected)
- **RHTPA 2.1.1** (h2 0.4.5 -- affected)

## Rationale

PSIRT assigned Affects Versions based on scan timing, not actual dependency analysis. Lock file inspection reveals:

1. **RHTPA 2.1.1 was missing**: PSIRT did not include 2.1.1 even though it ships the same vulnerable h2 0.4.5 as 2.1.0.
2. **RHTPA 2.2.0 was incorrectly included**: PSIRT included 2.2.0, but the Cargo.lock at source tag v0.4.5 shows h2 0.4.8, which is the fixed version. The 2.2.x stream was never vulnerable.

This is an unscoped issue (no stream suffix), so the correction applies across all streams. The corrected Affects Versions are scoped to only the 2.1.x stream versions, since no 2.2.x versions are affected.

## Jira Update (proposed)

```
Field: versions (Affects Versions)
Action: Set to [RHTPA 2.1.0, RHTPA 2.1.1]
Removes: RHTPA 2.2.0
Adds: RHTPA 2.1.1
```

## Sibling/Duplicate Check (Step 4)

JQL search for sibling issues with the same CVE label returned **no results** (no sibling issues exist). Since this is an unscoped issue and no siblings exist, no duplicate detection or cross-stream companion linking is needed.
