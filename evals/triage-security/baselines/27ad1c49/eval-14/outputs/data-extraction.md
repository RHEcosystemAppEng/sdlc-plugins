# Step 1 -- Data Extraction: TC-8005

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
| Upstream fix PR | (none) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Issue summary contains stream suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Triage is **scoped** to the 2.2.x stream only
- Steps 3 and 4 will apply only to 2.2.x versions; cross-stream impact (2.1.x) handled via Case A

## Ecosystem Detection

- Vulnerable library: openssl-libs
- Ecosystem: **RPM** (system package in container images)
- Category: System package
- Remediation tasks per stream: **1** (Konflux release repo fix only)
- Lock file configured: `rpms.lock.yaml` (per 2.2.x stream Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml`

## Deployment Context Lookup

- Affected component label: `pscomponent:org/rhtpa-server`
- Source Repositories table match: no exact match found for `org/rhtpa-server`
- Deployment context: **upstream** (default, since no match in Source Repositories)
- Note: The Source Repositories table does not include a Deployment Context column; coordination guidance will be omitted per backward compatibility rules
