# Step 1 -- Data Extraction

## Issue: TC-8005

**CVE-2026-40215** -- openssl-libs Buffer over-read in X.509 certificate verification [rhtpa-2.2]

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | **2.2.x** (scoped -- mapped from summary suffix [rhtpa-2.2] to Version Streams table entry for 2.2.x at rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Status | New |
| Upstream fix PR | (none in remote links) |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL (RHSA) | https://access.redhat.com/errata/RHSA-2026:4021 |
| Existing comments | (none) |

## Ecosystem Detection

| Attribute | Value |
|-----------|-------|
| Ecosystem | **RPM** (system package) |
| Category | System package -- 1 remediation task per stream (Konflux release repo fix) |
| Lock file | rpms.lock.yaml |
| Check command | `git show <tag>:rpms.lock.yaml \| grep 'openssl-libs'` |
| Upstream Branch | (not applicable -- RPM ecosystem has no upstream branch in Ecosystem Mappings) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream
in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is **scoped** to the 2.2.x stream only. Other streams (e.g., 2.1.x) are out
of scope for this issue but may be checked for cross-stream impact (Case A).

## Deployment Context

| Repository | Deployment Context |
|------------|--------------------|
| rhtpa-backend | upstream (default -- no Deployment Context column in Source Repositories table) |

## Vulnerability Description

A buffer over-read vulnerability exists in openssl-libs versions before 3.0.7-28.el9_4.
The flaw is in the `X509_verify_cert()` code path where the extension parser does not
properly validate the length field of a Subject Alternative Name extension. A remote
attacker can craft a certificate with a malformed extension that triggers an out-of-bounds
read, potentially leaking sensitive memory contents or causing a crash. The fix adds
bounds checking before reading extension data.

## Notes

- The PSIRT-assigned Affects Versions field shows "RHTPA 2.0.0" which does not correspond
  to any version in the 2.2.x stream. This will need correction in Step 3.
- CVSS 7.1 (High) meets the embargo check threshold (>= 7.0). Step 1.7 would present
  an embargo warning gate if an embargo policy URL is configured.
