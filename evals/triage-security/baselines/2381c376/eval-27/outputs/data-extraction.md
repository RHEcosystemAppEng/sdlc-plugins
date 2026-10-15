# Step 1 -- Data Extraction: TC-8051

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Advisory URL | (none) |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is **scoped** to the 2.2.x stream only. Steps 3 and 4 will apply only to versions within this stream.

## Ecosystem Detection

The vulnerable library `rustls` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table includes Cargo:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Ecosystem: **Cargo** (source dependency). Remediation follows the source dependency path (2 tasks per stream: upstream fix + downstream propagation).

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (default, since no Deployment Context column is present in the Source Repositories table).
