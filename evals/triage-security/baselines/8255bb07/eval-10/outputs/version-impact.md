# Step 2 -- Version Impact Analysis: TC-8020

## CVE Details

- **CVE**: CVE-2026-55123
- **Library**: tokio
- **Fix threshold**: >= 1.42.0
- **Ecosystem**: Cargo (`Cargo.lock`)

## Version Impact Table

| Version | Stream | Build Tag | tokio version | Affected? | Notes |
|---------|--------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | v0.3.8 | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | v0.3.12 | 1.40.0 | **YES** | 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | v0.4.5 | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | v0.4.8 | 1.41.1 | **YES** | 1.41.1 < 1.42.0 |

## Cross-Stream Impact Summary

The issue is scoped to stream **rhtpa-2.2** (2.2.x), but the version impact analysis
reveals that stream **rhtpa-2.1** (2.1.x) is also affected:

- **rhtpa-2.2 (in scope)**: All versions (RHTPA 2.2.0, 2.2.1) ship tokio 1.41.1, which is below the fix threshold of 1.42.0. **Affected.**
- **rhtpa-2.1 (out of scope)**: All versions (RHTPA 2.1.0, 2.1.1) ship tokio 1.40.0, which is below the fix threshold of 1.42.0. **Affected.**

## Sibling CVE Jira Search (Step 4)

JQL query: `project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This means stream rhtpa-2.1 is affected but has no CVE Jira -- triggering Case B
(preemptive remediation) in addition to Case A (standard remediation for rhtpa-2.2).

## Source Pinning Details

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | Source Pinning Method |
|---------|-----------|----------------------|
| RHTPA 2.1.0 | v0.3.8 | `artifacts.lock.yaml` (download URL contains tag) |
| RHTPA 2.1.1 | v0.3.12 | `artifacts.lock.yaml` (download URL contains tag) |

- Upstream branch: `release/0.3.z`

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | Source Pinning Method |
|---------|-----------|----------------------|
| RHTPA 2.2.0 | v0.4.5 | `artifacts.lock.yaml` (download URL contains tag) |
| RHTPA 2.2.1 | v0.4.8 | `artifacts.lock.yaml` (download URL contains tag) |

- Upstream branch: `release/0.4.z`
