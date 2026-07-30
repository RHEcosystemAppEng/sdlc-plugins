# Step 1 -- Data Extraction: TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only. Steps 3 and 4 will be scoped to this stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings in the security matrix, the ecosystem is **Cargo**. Cargo is a source dependency ecosystem, so remediation requires **2 tasks per affected stream**: upstream backport + downstream propagation (with downstream blocked by upstream).

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. No explicit Deployment Context column is present, so the default context is **upstream**.

## Version Impact Analysis (Step 2)

### Stream 2.1.x (rhtpa-release.0.3.z) -- outside issue scope, for cross-stream awareness

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | 0.11.12 (same as v0.4.8, retag) | YES (< 0.11.14) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14, fixed) |

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x stream configured. Based on lock file analysis scoped to stream 2.2.x:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is the fixed version.

### Cross-Stream Impact (Case A)

This is a scoped issue (stream 2.2.x). The version impact analysis reveals that stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9). This triggers Case A: a cross-stream impact comment should be posted, and proactive remediation tasks should be created for 2.1.x if no sibling CVE Jira exists for that stream.
