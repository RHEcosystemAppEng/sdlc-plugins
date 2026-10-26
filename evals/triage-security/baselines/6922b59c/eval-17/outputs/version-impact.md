# Step 2 -- Version Impact Analysis

## CVE-2026-31812: quinn-proto (affected: versions before 0.11.14)

### Version Impact Table

| Stream | Version | Build Tag | quinn-proto version | Affected? | Notes |
|--------|---------|-----------|---------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Type: source dependency (Rust crate)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |

### Stream Impact Summary

- **Stream 2.2.x** (issue scope): Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14). The upstream branch `release/0.4.z` already has the fix at v0.4.11+.
- **Stream 2.1.x** (cross-stream): ALL versions (2.1.0, 2.1.1) are affected. Both ship quinn-proto 0.11.9 which is within the vulnerable range. The upstream branch `release/0.3.z` does NOT yet have the fix (latest tag v0.3.12 ships 0.11.9).

### Affects Versions Correction Needed

The Jira issue currently has `Affects Versions: RHTPA 2.0.0`. This is incorrect -- there is no `2.0.x` stream configured. Based on lock file evidence, the correct Affects Versions for the scoped stream (2.2.x) should include RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2. RHTPA 2.0.0 should be removed. Versions 2.2.3 and 2.2.4 are NOT affected and should not be listed.

### Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x (from `[rhtpa-2.2]` suffix), but stream 2.1.x is also affected. Case A applies: a cross-stream impact comment should be posted, and preemptive remediation tasks should be created for stream 2.1.x if no sibling CVE Jira exists for that stream.
