# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | Outside issue scope |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | Outside issue scope |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | In scope |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | In scope |

Fix threshold: 1.42.0 (from CVE data and external enrichment)

## Cross-Stream Impact Summary

- **Current stream (rhtpa-2.2)**: 2 versions affected (RHTPA 2.2.0, RHTPA 2.2.1) -- tokio 1.41.1 < 1.42.0
- **Other stream (rhtpa-2.1)**: 2 versions affected (RHTPA 2.1.0, RHTPA 2.1.1) -- tokio 1.40.0 < 1.42.0

## Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result for stream rhtpa-2.1**: No sibling Vulnerability issues found. No CVE Jira exists for stream rhtpa-2.1.

## Conclusion

The issue is scoped to stream rhtpa-2.2, but cross-stream analysis reveals stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0 fix threshold). No CVE Jira exists for rhtpa-2.1. This triggers:
- **Case A**: Standard remediation tasks for the current stream (rhtpa-2.2)
- **Case A cross-stream**: Preemptive remediation tasks for the affected stream without a CVE Jira (rhtpa-2.1)
