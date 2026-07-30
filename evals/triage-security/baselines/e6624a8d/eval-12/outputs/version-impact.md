# Step 2 -- Version Impact Analysis

## CVE-2026-48901 (h2 < 0.4.8)

Enriched fix threshold from Step 1.5: **h2 < 0.4.8 is affected; h2 >= 0.4.8 is not affected**

Issue stream scope: **2.2.x** (from suffix [rhtpa-2.2])

### Version Impact Table

#### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

#### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Summary

- **Stream 2.2.x (scoped)**: **NOT affected** -- all versions ship h2 >= 0.4.8
- **Stream 2.1.x (cross-stream)**: **AFFECTED** -- all versions ship h2 0.4.5, which is below the fix threshold of 0.4.8

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Profile: production (h2 is an HTTP/2 runtime dependency)

  Stream 2.1.x: h2 0.4.5 at all versions (v0.3.8, v0.3.12)
  Stream 2.2.x: h2 0.4.8+ at all versions (already at or above fix threshold)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at Branch HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|-------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | **NO** -- branch still ships vulnerable h2 |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES -- branch ships h2 >= 0.4.8 |

### Triage Outcome

The issue is scoped to stream 2.2.x, which is **not affected**. However, stream 2.1.x **is affected** (cross-stream impact).

This triggers:
1. **Affects Versions correction** (Step 3): PSIRT assigned RHTPA 2.2.0, but 2.2.x is not affected. Affects Versions should be corrected to reflect 2.1.x versions (RHTPA 2.1.0, RHTPA 2.1.1) or cleared for the 2.2.x-scoped issue.
2. **Case A** (cross-stream impact): post cross-stream impact comment noting 2.1.x is affected.
3. **Preemptive remediation**: create remediation tasks for stream 2.1.x since it lacks its own CVE Jira.
4. For the scoped stream 2.2.x: recommend closing as Not a Bug with VEX justification "Component not Present" (the vulnerable version of h2 is not present in any 2.2.x release).
