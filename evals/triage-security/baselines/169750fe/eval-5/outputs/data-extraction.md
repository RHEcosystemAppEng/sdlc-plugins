# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | N/A (RPM system package -- fix via RHSA errata) |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: openssl-libs
- Ecosystem: **RPM** (system package in container images)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for 2.2.x stream)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation task count per stream: **1** (Konflux release repo fix only -- no upstream+downstream split for system packages)
