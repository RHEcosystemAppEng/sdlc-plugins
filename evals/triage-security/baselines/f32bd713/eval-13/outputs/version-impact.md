# Step 2 -- Version Impact Analysis for TC-8001

## CVE-2026-31812 (quinn-proto < 0.11.14)

### Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same source commit v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Enriched Fix Threshold

- Jira description: < 0.11.14 (fixed in 0.11.14)
- External CVE data (MITRE/OSV): would be queried for cross-validation in interactive mode
- Fix threshold used: **0.11.14** (versions < 0.11.14 are affected)

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock at workspace level)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

### Retag Handling

- Version 2.2.2 (tag v0.4.9) is a retag of version 2.2.1 (tag v0.4.8)
- Both share the same backend source commit: `v0.4.8`
- Lock file check skipped for 2.2.2; result carried forward from 2.2.1: quinn-proto 0.11.12 (AFFECTED)

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |

### Stream-Scoped Impact Summary

**In-scope stream (2.2.x):**
- Affected versions: 2.2.0, 2.2.1, 2.2.2
- Not affected: 2.2.3, 2.2.4
- Upstream fix available on release/0.4.z: **YES** -- use dependency bump variant

**Out-of-scope stream (2.1.x) -- cross-stream impact (Case A):**
- Affected versions: 2.1.0, 2.1.1
- Upstream fix available on release/0.3.z: **NO** -- requires upstream backport
- No stream-specific CVE Jira exists for 2.1.x -- preemptive remediation tasks needed

### Affects Versions Correction (for Step 3)

PSIRT assigned "RHTPA 2.0.0" as Affects Versions. Based on version impact analysis:

- **RHTPA 2.0.0** -- no such version exists in the supportability matrix or Version Streams. Must be removed.
- Correct Affects Versions for stream 2.2.x (in-scope): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- Versions RHTPA 2.2.3 and RHTPA 2.2.4 ship the fixed version and must NOT be in Affects Versions.
