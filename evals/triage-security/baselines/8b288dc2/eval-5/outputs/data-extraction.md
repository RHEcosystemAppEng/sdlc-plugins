# Step 1 -- Data Extraction for TC-8005

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
| Upstream fix PR | (none -- advisory-only, no upstream PR link) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

Triage is scoped to the 2.2.x stream only. Versions from other streams (e.g., 2.1.x) are out of scope for Affects Versions correction and remediation task creation on this issue, but are noted for cross-stream impact (Case B).

## Ecosystem Detection

Library: openssl-libs
Ecosystem: **RPM** (system package in container image)

The RPM ecosystem is configured in the 2.2.x stream's security-matrix.md Ecosystem Mappings table with:
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml`

Since an RPM lock file is configured, the investigation method is lock file inspection (rpms.lock.yaml). Remediation follows the single-task flow (Konflux repo fix only; no upstream backport task needed).

## Deployment Context Lookup

Repository `rhtpa-backend` found in Source Repositories table. The Deployment Context column is absent from the Source Repositories table, so the deployment context defaults to **upstream**.
