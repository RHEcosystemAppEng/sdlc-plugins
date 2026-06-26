# Version Impact Analysis — CVE-2026-55123 (tokio)

## Fix Threshold

- Affected range: versions before 1.42.0
- Fixed version: **1.42.0**

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

## Cross-Stream Impact Summary

- **rhtpa-2.2** (issue stream): RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1 < 1.42.0)
- **rhtpa-2.1** (other stream): RHTPA 2.1.0 and 2.1.1 are affected (tokio 1.40.0 < 1.42.0)

Stream rhtpa-2.1 is **outside** the scope of TC-8020 (which is scoped to `[rhtpa-2.2]`) but is confirmed affected by lock file analysis.

## Sibling CVE Jira Search (Step 4)

JQL search for sibling Vulnerability issues with label `CVE-2026-55123` in stream rhtpa-2.1:

```
project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"
```

**Result**: No sibling CVE Jira found for stream rhtpa-2.1.

This triggers Step 7 Case B — preemptive remediation tasks must be created for the rhtpa-2.1 stream.
