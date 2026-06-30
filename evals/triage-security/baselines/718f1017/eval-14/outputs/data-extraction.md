# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- Issue stream scope: **2.2.x only** (scoped issue -- Steps 2-7 analyze only the 2.2.x stream)

## Ecosystem Detection

- Library: openssl-libs
- Ecosystem: **RPM** (system package in container image)
- Lock File: `rpms.lock.yaml` (configured in 2.2.x stream Ecosystem Mappings)
- Check Command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation path: 1 task (Konflux repo fix -- no upstream step needed for RPM ecosystem)

## Notes

- The PSIRT-claimed Affects Version "RHTPA 2.0.0" does not match any configured Version Stream (no 2.0.x stream exists). This will need correction in Step 3.
- The issue is scoped to stream 2.2.x per the `[rhtpa-2.2]` suffix, so only versions in the 2.2.x stream are analyzed for Affects Versions correction.
