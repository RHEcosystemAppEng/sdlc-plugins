# Version Impact Analysis — CVE-2026-55123 (tokio)

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

Fix threshold: 1.42.0 (from Jira description, cross-validated with external CVE databases)

All versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Summary

| Stream | Versions Affected | tokio version(s) | In Issue Scope? |
|--------|-------------------|-------------------|-----------------|
| rhtpa-2.2 (2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1 | 1.41.1 | YES (issue scoped to [rhtpa-2.2]) |
| rhtpa-2.1 (2.1.x) | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0 | NO (different stream) |

Stream rhtpa-2.1 is also affected but is outside the scope of TC-8020. This triggers Case B (cross-stream impact with preemptive remediation).

## Dependency Chain Context

```
Dependency chain for tokio (Cargo):
  backend (workspace) -> tokio (runtime dependency)
  Profile: production (tokio is a core async runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Source repo: rhtpa-backend
```

tokio is a direct dependency of the backend workspace and is present in all versions across both streams.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix available (tokio-rs/tokio#7001) |
| 2.1.x | Cargo | release/0.3.z | Upstream fix available (tokio-rs/tokio#7001) |

The upstream fix (tokio-rs/tokio#7001) bumps tokio to 1.42.0. Both streams need to pick up this fix by updating tokio in the Cargo.lock on their respective upstream branches.

## Affects Versions Correction

The issue is scoped to stream rhtpa-2.2 (2.2.x). Affects Versions correction is scoped to this stream only.

- Current Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
- Proposed Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

PSIRT-assigned Affects Versions are **correct** for the scoped stream. No correction needed.

## Sibling CVE Jira Check (Step 4)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**No sibling Vulnerability issues found** for CVE-2026-55123 in any stream.

This means:
- No same-stream duplicate exists (no duplicate closure needed)
- No cross-stream companion exists for stream rhtpa-2.1 (triggers preemptive task creation in Case B)
