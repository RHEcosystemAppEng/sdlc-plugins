# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Stream scope | 2.1.x (mapped from suffix `[rhtpa-2.1]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Ecosystem | Cargo (Rust crate) |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Upstream fix PR | tokio-rs/tokio#7001 (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | GHSA-2026-tk91-v5pp (https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Existing comments | None |
| Existing issue links | None |

## Labels

- CVE-2026-55123
- pscomponent:org/rhtpa-server

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. This maps to:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

The issue is **scoped** to stream 2.1.x only. Steps 2-7 will analyze only versions within this stream.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. The ecosystem is **Cargo**, as confirmed by the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

For a Cargo (source dependency) ecosystem, remediation would normally require **two tasks**: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the Konflux release repo). However, see reconciliation analysis -- Step 4.4 finds an existing preemptive task.

## Custom Fields

| Custom Field | ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-tk91-v5pp | https://github.com/advisories/GHSA-2026-tk91-v5pp | GitHub Advisory |
| CVE-2026-55123 | https://www.cve.org/CVERecord?id=CVE-2026-55123 | CVE Record |
| tokio-rs/tokio#7001 | https://github.com/tokio-rs/tokio/pull/7001 | Upstream fix PR |
