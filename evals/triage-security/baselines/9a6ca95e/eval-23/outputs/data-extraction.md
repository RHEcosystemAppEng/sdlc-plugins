# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only. Affects Versions corrections and remediation tasks will be limited to 2.2.x versions. Cross-stream impact on 2.1.x is handled separately (Case B).

## Ecosystem Detection

Vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
Upstream Branch: `release/0.4.z` (for 2.2.x stream)

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to source repository **rhtpa-backend**. From the Source Repositories table in CLAUDE.md:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

Deployment context for this CVE: **customer-shipped**

This means coordination with Product Security is required for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis

### Stream 2.2.x (scoped -- primary analysis)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Stream 2.1.x (cross-stream impact)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (scoped to 2.2.x, based on lock file analysis)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not match any version in the supportability matrix. The actual affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2 (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 which is the fixed version.
- The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a different stream and would be tracked by a companion/sibling CVE issue.

### Cross-Stream Impact Summary

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9, which is < 0.11.14). This triggers Case B: cross-stream impact handling. If no sibling CVE Jira exists for the 2.1.x stream, preemptive remediation tasks should be created.
