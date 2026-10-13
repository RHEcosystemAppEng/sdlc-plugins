# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to versions in this stream.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (dependency bump + downstream propagation, since upstream fix is available)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z` (for 2.2.x stream)

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** in the Source Repositories table.

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The deployment context **customer-shipped** was found in the Source Repositories table's Deployment Context column. This value will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | at fix threshold |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

The 2.2.x upstream branch (`release/0.4.z`) already ships quinn-proto 0.11.14 (the fixed version). Remediation for 2.2.x uses the dependency bump variant (no upstream backport needed -- `cargo update` is sufficient).

The 2.1.x upstream branch (`release/0.3.z`) still ships quinn-proto 0.11.9 (vulnerable). Remediation for 2.1.x would require an upstream backport if it were in scope.

### Cross-Stream Impact

The issue is scoped to 2.2.x, but stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This triggers Case A (cross-stream impact) in Step 8 -- a cross-stream impact comment will be posted, and preemptive remediation tasks may be created for 2.1.x if no sibling CVE Jira exists for that stream.
