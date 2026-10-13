# Step 1 -- Data Extraction: TC-8005

## Parsed CVE Data

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
| Upstream fix PR | None (no GitHub PR in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for 2.2.x)
- Triage is scoped to the 2.2.x stream

## Ecosystem Detection

- Package: openssl-libs (RPM system package)
- Ecosystem: **RPM**
- Category: System package
- Remediation tasks per stream: **1** (Konflux release repo fix only -- no upstream step needed)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for both streams)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Deployment Context

- Affected repository (from component label): org/rhtpa-server
- Source Repositories table match: rhtpa-backend
- Deployment Context column: **absent** (backward compatibility -- no Deployment Context column in Source Repositories table)
- Default deployment context: `upstream`
- Coordination guidance: omitted (Deployment Context column absent)
