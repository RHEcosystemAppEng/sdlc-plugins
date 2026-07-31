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
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(no comments)_ |
| CVSS | 7.1 (High) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table.
Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

- **Ecosystem**: RPM (system package)
- **Category**: System package -- remediation produces 1 task per stream (Konflux release repo fix only)
- **Lock file**: rpms.lock.yaml (configured in 2.2.x stream Ecosystem Mappings)
- **Check command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
