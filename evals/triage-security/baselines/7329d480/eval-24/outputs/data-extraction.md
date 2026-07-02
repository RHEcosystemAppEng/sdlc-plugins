# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
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
| Ecosystem | Cargo |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is scoped to the 2.2.x stream only.

## Ecosystem Detection

quinn-proto is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. This is a source dependency ecosystem, so remediation (if needed) follows the two-task pattern: upstream backport + downstream propagation.

## Version Impact Analysis

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|--------|-----------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version |

## Affects Versions Correction

The PSIRT-assigned Affects Versions field is **RHTPA 2.0.0**, which does not correspond to any configured version stream (only 2.1.x and 2.2.x exist). Based on the version impact analysis for the scoped stream (2.2.x):

- **Remove**: RHTPA 2.0.0 (does not exist as a supported version)
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, the fixed version).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Pinned Version | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

## Cross-Stream Impact

The issue is scoped to 2.2.x, but the version impact analysis reveals that stream **2.1.x** is also affected. All versions in stream 2.1.x (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). This triggers Case B (cross-stream impact with preemptive remediation).
