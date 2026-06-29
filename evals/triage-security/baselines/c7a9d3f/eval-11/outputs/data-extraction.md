# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Jira Issue Key | TC-8021 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (PS Component label) | pscomponent:org/rhtpa-server |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |
| Product version (PSIRT-claimed, summary suffix) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Upstream fix PR | tokio-rs/tokio#7001 (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

The issue is **stream-scoped** to `rhtpa-2.1` (the 2.1.x stream). Steps 2-7 will be scoped to this stream only.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. From the security-matrix.md Ecosystem Mappings table for the 2.1.x stream:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

Ecosystem: **Cargo** (Rust crate). Lock file: `Cargo.lock`. This means remediation would normally produce two tasks (upstream backport + downstream propagation) -- but see reconciliation analysis.

## Labels

- CVE-2026-55123
- pscomponent:org/rhtpa-server

## Remote Links

1. [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) -- GitHub Advisory
2. [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) -- CVE Record
3. [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) -- Upstream fix PR

## Existing Preemptive Task Context

The issue description notes that a proactive remediation task TC-8022 already exists for this stream (rhtpa-2.1), created by a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). This will be addressed formally in Step 4.4 (preemptive task reconciliation).
