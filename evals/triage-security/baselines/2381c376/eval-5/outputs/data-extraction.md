# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-40215 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable package | openssl-libs | Description text |
| Affected version range | versions before 3.0.7-28.el9_4 | Description text |
| Fixed version | 3.0.7-28.el9_4 | Description text |
| CVSS | 7.1 (High) | Description text |
| Upstream fix PR | (none) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 | Remote links (RHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links (cve.org) |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comments |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 8 are scoped to this stream only. Cross-stream impact on 2.1.x is handled via Case A.

## Ecosystem Detection

- Package: openssl-libs (RPM system package)
- Ecosystem: **RPM**
- Category: **System package** -- 1 remediation task per affected stream
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)
