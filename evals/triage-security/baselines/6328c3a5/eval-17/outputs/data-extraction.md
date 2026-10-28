# Step 1 -- Data Extraction

## Parsed CVE Data Table

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is **scoped to stream 2.2.x**. Steps 3 and 4 will apply only to versions within this stream. Cross-stream impact on 2.1.x is handled by Case A in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** as an ecosystem with:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z` (for 2.2.x stream)

**Ecosystem classification**: Source dependency (Cargo) -- produces 2 remediation tasks per stream (dependency bump + downstream propagation, since Step 2.5 confirms fix is available upstream).

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. The Deployment Context column is absent from the mock configuration, so the default deployment context is **upstream**.

## Affects Versions Discrepancy

PSIRT assigned `RHTPA 2.0.0` as the Affects Version, but there is no `2.0.x` stream configured in the Version Streams table. This is incorrect and will need correction in Step 3 based on version impact analysis results.
