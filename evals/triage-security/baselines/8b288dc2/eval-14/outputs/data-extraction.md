# Step 1 -- Data Extraction: TC-8005

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | _(none)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Triage is scoped to the 2.2.x stream only

## Ecosystem Detection

- Library: openssl-libs (system RPM package)
- Ecosystem: **RPM**
- Lock file: `rpms.lock.yaml` (configured in 2.2.x stream Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Deployment Context

- Repository: rhtpa-backend (from pscomponent:org/rhtpa-server)
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)
