# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | Cross-stream (outside issue scope) |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | Cross-stream (outside issue scope) |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | Within issue scope |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | Within issue scope |

## Fix Threshold

- **Affected range**: versions before 1.42.0
- **Fixed version**: 1.42.0
- All versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact

The issue is scoped to stream **rhtpa-2.2** (from summary suffix `[rhtpa-2.2]`).

However, version impact analysis reveals that stream **rhtpa-2.1** is also affected:
- RHTPA 2.1.0 ships tokio 1.40.0 (< 1.42.0 threshold) -- **AFFECTED**
- RHTPA 2.1.1 ships tokio 1.40.0 (< 1.42.0 threshold) -- **AFFECTED**

### Sibling CVE Jira Search

JQL query for sibling issues:
```
project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"
```

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This triggers **Case B** (preemptive remediation) for stream rhtpa-2.1.

## Ecosystem Details

- **Ecosystem**: Cargo
- **Lock file**: Cargo.lock
- **Source repository**: backend
- **Upstream branch (2.1.x)**: release/0.3.z
- **Upstream branch (2.2.x)**: release/0.4.z
