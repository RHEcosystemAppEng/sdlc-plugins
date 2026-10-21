# Step 2 -- Version Impact Analysis

## Matrix Staleness Check (Step 0.3)

The security matrix file has a `Last-Updated` timestamp of `2026-06-28T10:00:00Z`.
Relative to today (2026-10-21), this is **115 days ago**, which exceeds the 14-day
staleness threshold. In a real triage, the engineer would be warned:

> Security matrix was last updated on 2026-06-28 (115 days ago). The matrix may
> not reflect recent releases. Options: Refresh now / Proceed anyway / Stop.

For this analysis, we proceed with the current matrix data.

## Supportability Matrix (Step 2.1)

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

## Version Impact Table (Steps 2.3 and 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.11.14 | NO | >= fix threshold |
| 2.2.x | 2.2.4 | 0.11.14 | NO | >= fix threshold |

**Fix threshold**: 0.11.14 (from Jira description; would be cross-validated with
MITRE CVE API and OSV.dev in Step 1.5 during interactive triage).

**Summary**: 5 of 7 supported versions ship a vulnerable version of quinn-proto.
- 2.1.x stream: ALL versions affected (2.1.0, 2.1.1)
- 2.2.x stream: 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2); fix present in 2.2.3+

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo ecosystem)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Present in all versions across both streams.
```

quinn-proto is a **direct** dependency of the backend workspace. Remediation is a
straightforward version bump (`cargo update -p quinn-proto`) -- no transitive
dependency coordination needed.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11, v0.4.12) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |

**2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14
(the fixed version) as evidenced by tags v0.4.11 and v0.4.12. Remediation for
this stream uses the **dependency bump** variant -- the fix is already available
and a `cargo update` is sufficient.

**2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 at
its latest tag (v0.3.12). The fix is **not yet available** on this branch.
Remediation requires an **upstream backport** to bump quinn-proto on
release/0.3.z, followed by downstream propagation.
