# Step 2 -- Version Impact Analysis

## CVE-2026-48901 (h2 < 0.4.8)

Fix threshold: **0.4.8** (from Step 1.5 external CVE data enrichment, cross-validated via MITRE CVE API and OSV.dev)

### Version Impact Table

#### Stream 2.2.x (issue scope: [rhtpa-2.2])

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.4.8 | NO | ships fix version |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.4.8 | NO | ships fix version |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.4.8 | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.4.9 | NO | ships post-fix version |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.4.9 | NO | ships post-fix version |

**Result**: No versions in the 2.2.x stream are affected. All versions ship h2 >= 0.4.8, which is at or above the fix threshold.

#### Stream 2.1.x (cross-stream analysis)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

**Result**: All versions in the 2.1.x stream are affected. Both versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

### Combined Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.2.x (scoped) | 0 of 5 | 5 of 5 |
| 2.1.x (cross-stream) | 2 of 2 | 0 of 2 |

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (Cargo)
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency)
```

The h2 crate is a direct dependency used for HTTP/2 protocol handling. Remediation is a straightforward version bump in Cargo.toml.

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command |
|--------|-----------|-----------------|---------------|
| 2.1.x | Cargo | release/0.3.z | `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | release/0.4.z | `git show release/0.4.z:Cargo.lock` |

Upstream fix PR: https://github.com/hyperium/h2/pull/800

### Cross-Stream Impact

The issue is scoped to stream **2.2.x**, which is NOT affected. However, the cross-stream analysis reveals that **stream 2.1.x IS affected** -- both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.

This triggers **Case A** (cross-stream impact) for proactive remediation of the 2.1.x stream, and **Case C** (no supported versions affected) for the scoped 2.2.x stream.
