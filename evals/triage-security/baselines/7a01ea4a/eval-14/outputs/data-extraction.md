# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z

Triage is scoped to the **2.2.x** stream only.

## Ecosystem Detection

- Ecosystem: **RPM** (system package -- openssl-libs is an OS-level package)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for this stream)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation model: **1 task** (Konflux repo fix; no upstream step for RPM packages)

## Deployment Context

- Repository `rhtpa-backend` found in Source Repositories table
- Deployment context: **upstream** (default -- no Deployment Context column configured)

## PSIRT Affects Versions Assessment

The PSIRT-assigned Affects Version `RHTPA 2.0.0` does not match any version in the 2.2.x supportability matrix. This will need correction in Step 3 after version impact analysis confirms which 2.2.x versions are actually affected.
