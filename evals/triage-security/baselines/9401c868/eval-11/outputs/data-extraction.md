# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x (mapped from summary suffix [rhtpa-2.1]) |
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

The issue summary contains the stream suffix `[rhtpa-2.1]`. This maps to the
`2.1.x` version stream in the Security Configuration Version Streams table:

- Stream: 2.1.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local Path: /home/dev/repos/rhtpa-release.0.3.z

This is a **scoped** issue -- Steps 3-4 apply only to the 2.1.x stream.

## Ecosystem Detection

The vulnerable library `tokio` is a Rust crate. The 2.1.x stream's Ecosystem
Mappings table lists Cargo as a supported ecosystem with:

- Repository: backend
- Lock File: Cargo.lock
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: release/0.3.z

Ecosystem classification: **Source dependency (Cargo)** -- produces 2 remediation
tasks per stream (upstream backport or dependency bump + downstream propagation).

## Configuration Extracted (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 |
| PS Component field | customfield_10669 |
| Stream field | customfield_10832 |
