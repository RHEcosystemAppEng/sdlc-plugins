# Version Impact Analysis — TC-8020

## CVE-2026-55123 (tokio < 1.42.0)

### Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

Fix threshold: **1.42.0** (from CVE record and advisory)

All versions across both streams ship tokio below the fix threshold (1.42.0).

### Cross-Stream Impact Summary

- **Current stream (rhtpa-2.2)**: 2 versions affected (2.2.0, 2.2.1) -- tokio 1.41.1 < 1.42.0
- **Other stream (rhtpa-2.1)**: 2 versions affected (2.1.0, 2.1.1) -- tokio 1.40.0 < 1.42.0

The issue is scoped to stream rhtpa-2.2. Cross-stream analysis reveals that stream
rhtpa-2.1 is **also affected** and ships an even older version of tokio (1.40.0 vs 1.41.1).

### Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This means stream rhtpa-2.1 has no CVE Jira tracking this vulnerability. Case A
(cross-stream preemptive remediation) applies -- preemptive tasks must be created
for stream rhtpa-2.1.

### Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Library | Fix Threshold |
|--------|-----------|-----------------|---------|---------------|
| 2.1.x | Cargo | release/0.3.z | tokio | 1.42.0 |
| 2.2.x | Cargo | release/0.4.z | tokio | 1.42.0 |

Upstream fix PR: [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001)
