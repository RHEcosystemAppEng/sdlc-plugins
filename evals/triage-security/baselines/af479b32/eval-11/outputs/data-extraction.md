# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams row: stream 2.1.x, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **rhtpa-2.1 only** (scoped issue -- Steps 3-4 apply to this stream only)

## Ecosystem Detection

- Vulnerable library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Source repository: rhtpa-backend

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column present in Source Repositories table)

## Configuration Validated (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

## Existing Preemptive Task (from Step 4.4 JQL)

A JQL search for `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returned:

- **TC-8022** -- Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
  - Status: Open
  - Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
  - Issue Links: Related to TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

This preemptive task was created during prior triage of TC-8020 (stream rhtpa-2.2) via Step 8 Case B cross-stream proactive remediation.
