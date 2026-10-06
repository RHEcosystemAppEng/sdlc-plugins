# Step 1 -- Data Extraction: TC-8005

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none) |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`
- Scope: **scoped** -- only analyze the 2.2.x stream

## Ecosystem Detection

- Library: openssl-libs (RPM system package)
- Ecosystem category: **System package** (RPM)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation tasks per stream: **1** (Konflux release repo fix only)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)

## Affects Versions Mismatch

The PSIRT-assigned Affects Versions field lists **RHTPA 2.0.0**, but no 2.0.x stream is configured in the Version Streams table. The issue summary suffix `[rhtpa-2.2]` scopes this to the **2.2.x** stream. The Affects Versions field needs correction based on version impact analysis in Step 2.
