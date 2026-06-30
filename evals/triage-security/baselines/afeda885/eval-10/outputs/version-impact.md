# Step 2 — Version Impact Analysis: CVE-2026-55123

## Fix Threshold

- Vulnerable library: tokio
- Affected range: versions before 1.42.0
- Fix threshold: **1.42.0**

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** | |

All versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

- **Issue scope**: stream rhtpa-2.2 (per summary suffix `[rhtpa-2.2]`)
- **In-scope affected versions**: RHTPA 2.2.0, RHTPA 2.2.1 (tokio 1.41.1)
- **Out-of-scope affected versions**: RHTPA 2.1.0, RHTPA 2.1.1 (tokio 1.40.0) — stream rhtpa-2.1 is also affected

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of 1.42.0. This stream is outside the current issue's scope but is confirmed affected by lock file analysis.

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) → tokio (direct runtime dependency)
  Ecosystem: Cargo
  Profile: production (tokio is a runtime dependency)
```

## Sibling CVE Jira Search Results

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.**

This means stream rhtpa-2.1 has no dedicated CVE Jira and requires preemptive remediation (Case B).
