# Step 2 -- Version Impact Analysis for CVE-2026-55123

## Fix Threshold

- Vulnerable library: tokio
- Affected range: versions before 1.42.0
- Fix threshold: **1.42.0**

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | 1.40.0 | **YES** | tokio 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | 1.40.0 | **YES** | tokio 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | 1.41.1 | **YES** | tokio 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | 1.41.1 | **YES** | tokio 1.41.1 < 1.42.0 |

## Cross-Stream Impact Summary

- **Issue stream (rhtpa-2.2):** RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1)
- **Other stream (rhtpa-2.1):** RHTPA 2.1.0 and 2.1.1 are also affected (tokio 1.40.0)
- Both streams ship tokio versions below the fix threshold of 1.42.0

## Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result:** No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This means:
- Stream rhtpa-2.2 has TC-8020 (the current issue)
- Stream rhtpa-2.1 has **no CVE Jira** -- triggers Case B preemptive remediation
