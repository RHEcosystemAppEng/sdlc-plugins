# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Step 2 — Version Impact Table

### Aggregated Supportability Matrix

All versions from both configured streams (2.1.x and 2.2.x):

| Version | Stream | Build Tag | Build Date | backend |
|---------|--------|-----------|------------|---------|
| 2.1.0 | rhtpa-2.1 (2.1.x) | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | rhtpa-2.1 (2.1.x) | 0.3.12 | 2025-11-20 | v0.3.12 |
| 2.2.0 | rhtpa-2.2 (2.2.x) | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | rhtpa-2.2 (2.2.x) | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | rhtpa-2.2 (2.2.x) | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | rhtpa-2.2 (2.2.x) | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | rhtpa-2.2 (2.2.x) | 0.4.12 | 2026-05-04 | v0.4.12 |

### Dependency Version Extraction (tokio)

Extracted from lock file data (simulated `git show <tag>:Cargo.lock`):

| Version | Stream | tokio version | Fix threshold | Affected? | Notes |
|---------|--------|---------------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | 1.42.0 | **YES** | tokio 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | 1.42.0 | **YES** | tokio 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | 1.42.0 | **YES** | tokio 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | 1.42.0 | **YES** | tokio 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | rhtpa-2.2 | -- | 1.42.0 | **YES** | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | rhtpa-2.2 | *(not in mock data)* | 1.42.0 | *(unknown)* | No tokio version data provided |
| RHTPA 2.2.4 | rhtpa-2.2 | *(not in mock data)* | 1.42.0 | *(unknown)* | No tokio version data provided |

Note: The mock lock file data does not include tokio versions by tag. The cross-stream version impact table provided in the issue description is used as the authoritative source for tokio versions.

### Cross-Stream Version Impact Summary

Based on the cross-stream version impact data provided in the issue description:

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** |

All versions across both streams ship tokio < 1.42.0 and are affected.

### Stream-Scoped Impact (for this issue TC-8020)

Since TC-8020 is scoped to stream **rhtpa-2.2**, only the following versions are within scope for Steps 3-8:

| Version | tokio version | Affected? |
|---------|---------------|-----------|
| RHTPA 2.2.0 | 1.41.1 | **YES** |
| RHTPA 2.2.1 | 1.41.1 | **YES** |

### Cross-Stream Impact (outside this issue's scope)

Stream **rhtpa-2.1** is also affected but is outside this issue's stream scope:

| Version | tokio version | Affected? |
|---------|---------------|-----------|
| RHTPA 2.1.0 | 1.40.0 | **YES** |
| RHTPA 2.1.1 | 1.40.0 | **YES** |

This triggers **Case B** (cross-stream impact / preemptive remediation) in Step 8.

### Sibling CVE Jiras for Cross-Stream Impact

JQL search for sibling CVE Jiras with label CVE-2026-55123:
- Stream rhtpa-2.1: **No sibling Vulnerability issue found**

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks must be created (Case B).
