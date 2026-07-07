# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (matched to rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | -- |
| Advisory URL | RHSA-2026:4021 (https://access.redhat.com/errata/RHSA-2026:4021) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). Triage is scoped to this stream only.

## Ecosystem Detection

The vulnerable package `openssl-libs` is an RPM system package. The 2.2.x stream's Ecosystem Mappings table lists:

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml \| grep 'openssl-libs'` |

Investigation method: rpms.lock.yaml inspection with optional SBOM verification via cosign.

## Remote Links

- [CVE-2026-40215](https://www.cve.org/CVERecord?id=CVE-2026-40215) -- CVE Record
- [RHSA-2026:4021](https://access.redhat.com/errata/RHSA-2026:4021) -- Red Hat Security Advisory

## Vulnerability Details

A buffer over-read in the `X509_verify_cert()` code path where the extension parser does not properly validate the length field of a Subject Alternative Name extension. A remote attacker can craft a certificate with a malformed extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash. The fix adds bounds checking before reading extension data.
