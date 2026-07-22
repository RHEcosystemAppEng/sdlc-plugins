# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(no comments)_ |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Streams entry: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: openssl-libs
- Ecosystem: **RPM** (system package in container image)
- Lock file: `rpms.lock.yaml` (configured in 2.2.x Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Deployment Context

- Affected repository: rhtpa-backend (from pscomponent:org/rhtpa-server)
- Source Repositories table: rhtpa-backend found
- Deployment Context column: absent (not configured in Source Repositories table)
- Result: default to `upstream`

## Affects Versions Discrepancy (preliminary)

- PSIRT assigned: **RHTPA 2.0.0**
- No 2.0.x stream exists in Version Streams configuration
- PSIRT version appears incorrect -- will be corrected in Step 3 based on version impact analysis scoped to 2.2.x stream
