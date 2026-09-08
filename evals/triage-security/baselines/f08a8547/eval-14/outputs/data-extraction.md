# Step 1 -- Data Extraction

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
| Due date | 2026-08-15 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`.
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is scoped to the **2.2.x** stream only.

## Ecosystem Detection

- **Ecosystem**: RPM (system package)
- **Lock file**: `rpms.lock.yaml` (configured in Ecosystem Mappings for stream 2.2.x)
- **Check command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- **Category**: System package -- produces 1 remediation task per stream (Konflux release repo fix only)

## Deployment Context

- Repository `rhtpa-backend` has deployment context: **upstream** (default, no explicit Deployment Context column present in Source Repositories table)
