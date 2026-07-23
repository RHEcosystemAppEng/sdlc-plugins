# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8050

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | < 0.5.2 (versions before 0.5.2) |
| Fixed version | 0.5.2 |
| Upstream fix PR | -- |
| Advisory URL | -- |
| CVE record URL | [CVE-2026-99001](https://www.cve.org/CVERecord?id=CVE-2026-99001) |
| Due date | 2026-08-01 |
| Existing comments | None |
| CVSS | 5.3 (Medium) |
| Status | New |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream from the Version Streams table in Security Configuration.

Issue stream scope: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

## Ecosystem Detection

The vulnerable library is **criterion**, a Rust crate. This maps to the **Cargo** ecosystem from the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

Since this is a source dependency ecosystem (Cargo), remediation will require **two tasks**: an upstream backport task and a downstream propagation subtask.
