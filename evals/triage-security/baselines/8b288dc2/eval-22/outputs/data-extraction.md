# Data Extraction — TC-8021

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8021 |
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affected Component | pscomponent:org/rhtpa-server |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | versions before 0.11.14 |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream Fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due Date | 2026-07-15 |
| Existing Comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). The issue is **stream-scoped** to 2.2.x only. Steps 3 and 4 will be scoped to this stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The Ecosystem Mappings tables in both stream matrices list **Cargo** as the ecosystem for the `backend` repository, with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

**Ecosystem**: Cargo (source dependency)

This means remediation will produce **two tasks** per affected stream: an upstream backport task and a downstream propagation subtask.

## Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server`, which corresponds to `rhtpa-backend` in the Source Repositories table. The Source Repositories table does **not** include a Deployment Context column. Per backward-compatibility rules, all repositories default to `upstream`. However, since the column is absent, coordination guidance is **omitted entirely** from remediation task descriptions.

## Version Impact Analysis (Step 2)

Using the mock lock file data (simulating `git show <tag>:Cargo.lock` output):

### Stream 2.1.x (rhtpa-release.0.3.z) — outside issue scope

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z) — issue scope

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 — same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fix threshold) |

### Summary

- **Stream 2.2.x (in-scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version.
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected. This triggers Case B (cross-stream impact).

## Matrix Staleness Check (Step 0.3)

The security matrix has `Last-Updated: 2026-06-28T10:00:00Z`, which is 3 days ago (current date: 2026-07-01). This is within the 14-day staleness threshold. No staleness warning required. Proceed with triage.
