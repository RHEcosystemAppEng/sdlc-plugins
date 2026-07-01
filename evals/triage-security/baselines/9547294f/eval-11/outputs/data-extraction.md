# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server |
| Affected Component | pscomponent:org/rhtpa-server |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.1 (customfield_10832) |
| Affects Versions (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 (< 1.42.0) |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-15 |
| Upstream Fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Existing Comments | None |
| Existing Issue Links | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream in the Security Configuration Version Streams table:

- Stream: 2.1.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local Path: /home/dev/repos/rhtpa-release.0.3.z

This issue is **scoped** to the 2.1.x stream only. Steps 2-8 will analyze only versions within this stream.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, this falls under the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z`
- Repository: backend
