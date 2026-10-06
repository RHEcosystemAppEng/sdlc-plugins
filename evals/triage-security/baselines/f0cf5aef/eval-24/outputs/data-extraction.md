# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**.
Issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)

## Deployment Context

Source Repositories table does NOT have a Deployment Context column.
Per backward compatibility rule: all repos default to `upstream`.
Coordination Guidance subsection is **omitted** from remediation task descriptions.

## Step 2 — Version Impact Analysis

### Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | fixed at 0.11.14 |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (assumed from lock file presence)
  Ecosystem: Cargo
  Profile: production

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

### Affects Versions Correction

- **Current** (PSIRT-assigned): RHTPA 2.0.0
- **Correct** (based on lock file evidence): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- RHTPA 2.0.0 does not match any configured version stream — incorrect assignment by PSIRT.
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

### Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x. Stream **2.1.x** is also affected:
- 2.1.0: quinn-proto 0.11.9 (vulnerable)
- 2.1.1: quinn-proto 0.11.9 (vulnerable)

The upstream fix is NOT present on release/0.3.z for stream 2.1.x.
Preemptive remediation tasks are required for the 2.1.x stream.

### Triage Outcome Summary

- **2.2.x** (in-scope stream): Versions 2.2.0–2.2.2 are affected, but the fix is already present in 2.2.3+ (quinn-proto 0.11.14). Upstream branch release/0.4.z already has the fix. No new remediation tasks needed for this stream — the fix has already been shipped.
- **2.1.x** (cross-stream, Case A): All versions affected (2.1.0, 2.1.1). Upstream branch release/0.3.z does NOT have the fix. Preemptive remediation tasks required.
