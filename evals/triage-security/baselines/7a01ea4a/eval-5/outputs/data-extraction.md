# Step 1 -- Data Extraction: TC-8005

## Parsed CVE Data

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
| Upstream fix PR | N/A |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 4 will be scoped to this stream only. Cross-stream impact on 2.1.x will be handled under Case B in Step 8.

## Ecosystem Detection

- Vulnerable library: openssl-libs
- Ecosystem: **RPM** (system package in container images)
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Upstream Branch: N/A (RPM ecosystem has no upstream branch)

RPM ecosystem produces a **single** remediation task (Konflux release repo fix). No upstream backport task is needed.

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
