# Step 2 -- Version Impact Analysis

## Supportability Matrix (Aggregated)

Loaded from two version streams configured in Security Configuration:

- **Stream 2.1.x**: rhtpa-release.0.3.z (local path: /home/dev/repos/rhtpa-release.0.3.z)
- **Stream 2.2.x**: rhtpa-release.0.4.z (local path: /home/dev/repos/rhtpa-release.0.4.z)

Matrix staleness check: Last-Updated timestamp is 2026-06-28T10:00:00Z, which is within the 14-day threshold. Proceeding without refresh.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

**Fix threshold used:** quinn-proto >= 0.11.14 (from Jira description; external CVE enrichment from MITRE/OSV not performed in this eval).

### Retag handling

- Version 2.2.2 (build 0.4.9) is a retag of 2.2.1 (build 0.4.8). Lock file check skipped; result carried forward from 2.2.1. quinn-proto version is 0.11.12, which is within the affected range (< 0.11.14).

### Dependency chain context

quinn-proto is a Cargo (Rust) crate. Based on the Ecosystem Mappings, the relevant lock file is `Cargo.lock` in the `backend` repository.

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: assumed direct dependency (lock file analysis via git show)
  Profile: production (quinn-proto is a QUIC transport dependency)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Pinned Version | quinn-proto at Latest | Fixed? |
|--------|-----------|-----------------|----------------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

### Analysis

- **Stream 2.2.x (release/0.4.z):** The upstream branch already ships quinn-proto 0.11.14 (the fixed version). Starting from build v0.4.11 (version 2.2.3), the fix is incorporated. Remediation for this stream uses the **dependency bump** variant -- the fix is available via `cargo update`.
- **Stream 2.1.x (release/0.3.z):** The upstream branch still ships quinn-proto 0.11.9, which is within the affected range. The fix is **NOT** available upstream on this branch. Remediation requires an **upstream backport** -- the dependency must be bumped on release/0.3.z before it can be propagated downstream.

## Summary

- **Total affected versions:** 5 (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2)
- **Total unaffected versions:** 2 (2.2.3, 2.2.4)
- **Streams with affected versions:** 2.1.x (all versions), 2.2.x (3 of 5 versions)
- **Issue stream scope:** 2.2.x -- this issue tracks remediation for the 2.2.x stream. Cross-stream impact on 2.1.x is handled via Case A (cross-stream impact comment + preemptive remediation tasks if no sibling CVE Jira exists).
