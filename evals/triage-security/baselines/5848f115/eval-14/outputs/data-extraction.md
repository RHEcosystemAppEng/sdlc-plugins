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
| Upstream fix PR | -- |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is scoped to the **2.2.x stream only**.

## Ecosystem Detection

- **Ecosystem**: RPM (system package)
- **Category**: System package
- **Lock File**: `rpms.lock.yaml`
- **Check Command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- **Remediation tasks per stream**: 1 (Konflux release repo fix only)

The RPM ecosystem is listed in the 2.2.x stream's Ecosystem Mappings table. Since RPM is a system package ecosystem (not a source dependency), remediation produces a single task per affected stream rather than the upstream + downstream pair used for source dependencies.

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table with no explicit Deployment Context column, so the default context is `upstream`.

## Remote Links

| Link | Type |
|------|------|
| https://www.cve.org/CVERecord?id=CVE-2026-40215 | CVE Record |
| https://access.redhat.com/errata/RHSA-2026:4021 | Red Hat Security Advisory |

## Vulnerability Description

A buffer over-read vulnerability in openssl-libs during X.509 certificate chain verification. A remote attacker can craft a certificate with a malformed Subject Alternative Name extension that triggers an out-of-bounds read in `X509_verify_cert()`, potentially leaking sensitive memory contents or causing a crash. The fix adds bounds checking before reading extension data.
