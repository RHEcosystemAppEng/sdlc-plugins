# Step 1 -- Data Extraction: TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8020 |
| **CVE ID** | CVE-2026-31812 |
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-server |
| **Vulnerable Library** | quinn-proto |
| **Affected Version Range** | versions before 0.11.14 (< 0.11.14) |
| **Fixed Version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Affects Versions (PSIRT-claimed)** | RHTPA 2.0.0 |
| **Due Date** | 2026-07-15 |
| **Assignee** | Unassigned |
| **Upstream Affected Component** | quinn-proto (customfield_10632) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to that stream, and Case A (cross-stream impact) will check whether other streams are also affected.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- quinn-proto is a Rust crate)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream Fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0042.html

## Deployment Context

Repository `rhtpa-backend` has deployment context: **upstream** (default, since no Deployment Context column present in Source Repositories table).

## Version Impact Analysis (Step 2)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Combined Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**, which does not correspond to any configured version stream (no 2.0.x stream exists). This is incorrect.

Since the issue is scoped to stream **2.2.x**, only 2.2.x versions should be set:
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which is the fixed version).

### Cross-Stream Impact

The issue is scoped to 2.2.x, but the version impact analysis shows that stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This triggers **Case A** (cross-stream impact) in Step 8.
