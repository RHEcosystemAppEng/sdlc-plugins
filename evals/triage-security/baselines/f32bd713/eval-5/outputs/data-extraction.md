# Step 1 — Data Extraction: TC-8005

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (matched from suffix [rhtpa-2.2] to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | N/A (system package — fix via RHSA errata) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Ecosystem | RPM (system package) |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the
**2.2.x** stream in the Version Streams table (Konflux release repo:
`git.example.com/rhtpa/rhtpa-release.0.4.z`). Triage is scoped to this stream
for Steps 3-8. All supported streams (2.1.x, 2.2.x) are analyzed in Step 2 for
cross-stream impact detection (Case A).

## Ecosystem Detection

The vulnerable package `openssl-libs` is an RPM system package. The 2.2.x
stream's Ecosystem Mappings table includes an RPM ecosystem row with:
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Upstream Branch: (none — RPM packages have no upstream branch)

Per the ecosystem classification table, RPM is a system package ecosystem,
producing **1 remediation task** per affected stream (Konflux release repo fix only).
