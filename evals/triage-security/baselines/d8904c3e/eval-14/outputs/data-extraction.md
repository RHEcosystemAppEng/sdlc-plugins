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
| Existing comments | (no comments) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream. This matches the configured Version Stream entry:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Issue stream scope**: 2.2.x (scoped -- triage applies only to this stream)

## Ecosystem Detection

- **Library**: openssl-libs
- **Ecosystem**: RPM (system package in container image)
- **Category**: System package
- **Remediation tasks per stream**: 1 (Konflux release repo fix only)
- **Lock file**: rpms.lock.yaml (configured in Ecosystem Mappings for 2.2.x stream)
- **Check command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Remote Links

| Title | URL |
|-------|-----|
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Red Hat Security Advisory | https://access.redhat.com/errata/RHSA-2026:4021 |

## Notes

- The PSIRT-assigned Affects Versions field lists "RHTPA 2.0.0" which does not correspond to any version in the 2.2.x stream supportability matrix. This will need correction in Step 3.
- The vulnerability is in the `X509_verify_cert()` code path where the extension parser does not properly validate the length field of a Subject Alternative Name extension. The fix adds bounds checking before reading extension data.
