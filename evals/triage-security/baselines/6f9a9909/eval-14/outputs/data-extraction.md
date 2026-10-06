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
| Upstream fix PR | -- |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **scoped** to the 2.2.x stream. Steps 3-4 will apply only to versions within this stream.

## Ecosystem Detection

- Vulnerable library: openssl-libs
- Ecosystem: **RPM** (system package in container images)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for the 2.2.x stream)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Classification: **System package** -- remediation produces 1 task per stream (Konflux release repo fix only)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column configured in Source Repositories)

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
