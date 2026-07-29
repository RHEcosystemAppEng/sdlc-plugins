# Step 1 -- Data Extraction

## Issue: TC-8060

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| CVE record URL | [CVE-2026-99010](https://www.cve.org/CVERecord?id=CVE-2026-99010) |
| Advisory URL | -- |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table.

- Stream suffix: `[rhtpa-2.2]`
- Matched stream: **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

Triage is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to versions within this stream.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- **Upstream Branch**: `release/0.4.z`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Deployment Context

The affected repository **rhtpa-backend** is listed in Source Repositories without a Deployment Context column. Defaulting to `upstream`.
