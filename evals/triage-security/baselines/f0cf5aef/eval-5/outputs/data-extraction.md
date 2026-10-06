# Step 1 -- Data Extraction: TC-8005

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream, which corresponds to the Konflux release repo `rhtpa-release.0.4.z` at `/home/dev/repos/rhtpa-release.0.4.z`.

## Ecosystem Detection

- **Ecosystem**: RPM (system package)
- **Lock file**: `rpms.lock.yaml`
- **Check command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- **Classification**: System package -- 1 remediation task per stream (Konflux release repo fix only; no upstream backport step)

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (default, as no Deployment Context column is present in the Source Repositories table).
