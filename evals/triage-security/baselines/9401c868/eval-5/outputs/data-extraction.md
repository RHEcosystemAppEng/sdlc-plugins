# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | N/A |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: openssl-libs
- Ecosystem: **RPM** (system package)
- Category: System package -- remediation produces **1 task** per stream (Konflux release repo fix only)
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no explicit Deployment Context column in Source Repositories table)
