# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-55123 |
| **Jira Key** | TC-8021 |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected component** | pscomponent:org/rhtpa-server (from label matching `pscomponent:` pattern) |
| **Product version (PSIRT-claimed)** | Stream suffix `[rhtpa-2.1]` -- maps to stream **2.1.x** |
| **Affects Versions (Jira field)** | RHTPA 2.1.0, RHTPA 2.1.1 |
| **Vulnerable library** | tokio |
| **Affected version range** | versions before 1.42.0 |
| **Fixed version** | 1.42.0 |
| **CVSS** | 8.1 (High) |
| **Upstream fix PR** | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| **Advisory URL** | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| **CVE record URL** | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| **Due date** | 2026-08-15 |
| **Assignee** | Unassigned |
| **Existing comments** | None |

## Custom Fields

| Field | Value |
|-------|-------|
| **customfield_10632** (Upstream Affected Component) | tokio |
| **customfield_10669** (PS Component) | pscomponent:org/rhtpa-server |
| **customfield_10832** (Stream) | rhtpa-2.1 |

## Remote Links

| URL | Type |
|-----|------|
| https://github.com/advisories/GHSA-2026-tk91-v5pp | GitHub Advisory |
| https://www.cve.org/CVERecord?id=CVE-2026-55123 | CVE Record |
| https://github.com/tokio-rs/tokio/pull/7001 | Upstream fix PR |

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.1]`
- **Parsed stream**: 2.1.x
- **Configured Version Streams**: 2.1.x, 2.2.x
- **Match**: Yes -- suffix `rhtpa-2.1` matches the configured **2.1.x** stream
- **Issue stream scope**: **2.1.x only** (scoped issue; Steps 3 and 4 are scoped to this stream)

## Ecosystem Detection

- **Library**: tokio
- **Component**: org/rhtpa-server (a Rust backend service per Repository Registry)
- **Ecosystem**: **Cargo** (Rust crate -- tokio is a Rust async runtime crate)
- **Lock file**: `Cargo.lock` (from Ecosystem Mappings for 2.1.x stream)
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.3.z` (for 2.1.x stream)
- **Repository**: backend

## Version Impact Analysis (Step 2)

The mock lock file data in the security matrix does not include explicit tokio version entries. However, based on the vulnerability description and the issue fixture stating that TC-8022 was already created as a preemptive remediation task for this CVE in the rhtpa-2.1 stream (from prior triage of TC-8020 for stream 2.2.x), the version impact analysis from the originating triage established that the 2.1.x stream is affected.

Based on the supportability matrix for stream 2.1.x:

| Version | Stream | Source Tag | tokio version | Affected? | Notes |
|---------|--------|------------|---------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | < 1.42.0 (vulnerable) | YES | Confirmed by prior cross-stream analysis |
| 2.1.1 | 2.1.x | `v0.3.12` | < 1.42.0 (vulnerable) | YES | Confirmed by prior cross-stream analysis |

The prior triage of TC-8020 (stream 2.2.x) performed cross-stream impact analysis (Step 7 Case B) and determined that the 2.1.x stream was also affected, leading to the creation of preemptive remediation task TC-8022.
