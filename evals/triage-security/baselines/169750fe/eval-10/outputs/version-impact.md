# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version     | Stream    | tokio version | Affected? | Notes |
|-------------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |       |

All supported versions across both configured streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

- **Issue scope**: rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`)
- **Current stream affected versions**: RHTPA 2.2.0, RHTPA 2.2.1 (tokio 1.41.1)
- **Other stream affected**: rhtpa-2.1 (RHTPA 2.1.0 and 2.1.1, tokio 1.40.0)
- **Fix threshold**: tokio >= 1.42.0

## Stream-by-Stream Breakdown

### Stream rhtpa-2.2 (issue scope)

| Version     | Build Tag | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.2.0 | v0.4.5    | 1.41.1        | YES       |
| RHTPA 2.2.1 | v0.4.8    | 1.41.1        | YES       |

- Ecosystem: Cargo
- Lock file: `Cargo.lock`
- Upstream branch: `release/0.4.z`
- Source repository: backend

### Stream rhtpa-2.1 (cross-stream impact)

| Version     | Build Tag | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | v0.3.8    | 1.40.0        | YES       |
| RHTPA 2.1.1 | v0.3.12   | 1.40.0        | YES       |

- Ecosystem: Cargo
- Lock file: `Cargo.lock`
- Upstream branch: `release/0.3.z`
- Source repository: backend

## Sibling CVE Jira Search

JQL search for sibling Vulnerability issues with label CVE-2026-55123:

- **Stream rhtpa-2.2**: TC-8020 (current issue) -- this is the scoped issue
- **Stream rhtpa-2.1**: **No sibling CVE Jira found** -- no Vulnerability issue exists for this stream

This triggers Case A (cross-stream impact with preemptive remediation) for stream rhtpa-2.1.
