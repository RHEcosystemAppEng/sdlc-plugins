# Step 1 -- Data Extraction: TC-8005

## Extracted CVE Data

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
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none in remote links) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

This issue is **stream-scoped** to the 2.2.x stream. Steps 3-8 apply only to versions within this stream.

## Ecosystem Detection

- Vulnerable library: openssl-libs (system RPM package)
- Ecosystem: **RPM**
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for both streams)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

RPM ecosystem produces a single remediation task (Konflux release repo fix). No upstream backport task needed.

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
