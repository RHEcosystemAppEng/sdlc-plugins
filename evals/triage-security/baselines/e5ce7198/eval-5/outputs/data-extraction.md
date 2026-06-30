# Step 1 -- Data Extraction for TC-8005

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | (none) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| CVSS | 7.1 (High) |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Triage is scoped to the 2.2.x stream for Affects Versions correction and remediation task creation

## Ecosystem Detection

- Vulnerable package: openssl-libs (system RPM package)
- Ecosystem: **RPM**
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- No upstream source repository (RPM system package -- fix happens directly in Konflux release repo)

## Notes

- The PSIRT-assigned Affects Versions ("RHTPA 2.0.0") does not match any configured stream (2.1.x or 2.2.x). This will be corrected in Step 3.
- CVSS 7.1 is High severity, which would trigger the Embargo Check (Step 1.7) if an embargo policy URL were configured. The Security Configuration does not include an Embargo policy URL, so Step 1.7 is skipped.
