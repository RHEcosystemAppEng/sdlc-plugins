# Step 1 -- Data Extraction for TC-8001

## Extracted CVE Data

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

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). Triage is scoped to the 2.2.x stream for Affects Versions correction (Step 3) and duplicate detection (Step 4).

However, per Important Rule 4, the version impact analysis (Step 2) checks ALL supported versions across ALL streams from the supportability matrix, including the 2.1.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the security-matrix.md configuration, this maps to the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch (2.2.x stream): `release/0.4.z`
- Repository: backend

As a source dependency ecosystem (Cargo), remediation will require **two tasks**: an upstream backport task and a downstream propagation subtask with a Blocks dependency.
