# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo |
| Affected repository | rhtpa-backend |
| Deployment context | customer-shipped |

## Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`. Looking up `rhtpa-backend` in the Source Repositories table from Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Because the context is `customer-shipped`, remediation tasks will include guidance to coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Stream Scope Resolution

The issue summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). Triage is scoped to this stream for Steps 3-4 (Affects Versions correction and duplicate/sibling checks). Cross-stream impact on 2.1.x will be handled via Case B in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both streams lists Cargo with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. This is a source dependency ecosystem, so remediation requires two tasks per affected stream: an upstream backport task and a downstream propagation subtask.

## Version Impact Analysis

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version |

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream configured. Scoped to the 2.2.x stream, the correct Affects Versions are:

- Current: [RHTPA 2.0.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version).

### Cross-Stream Impact

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This triggers Case B (cross-stream impact) in Step 8. Since this issue is scoped to 2.2.x, the 2.1.x impact will be handled via preemptive remediation tasks or companion CVE Jiras.
