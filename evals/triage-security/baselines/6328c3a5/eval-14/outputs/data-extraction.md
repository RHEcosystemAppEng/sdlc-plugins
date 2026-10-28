# Step 1 -- Data Extraction

## Issue: TC-8005

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
| Due date | 2026-08-15 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none) |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`.
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is scoped to the **2.2.x** stream only.

## Ecosystem Detection

Library `openssl-libs` is an RPM system package.
Ecosystem Mappings for the 2.2.x stream configure:
- Ecosystem: RPM
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

Classification: **System package** -- remediation produces 1 task per affected stream (Konflux release repo fix).

## Vulnerability Description

A buffer over-read in `X509_verify_cert()` code path where the extension parser does not properly validate the length field of a Subject Alternative Name extension. A remote attacker can craft a certificate with a malformed extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash. The fix adds bounds checking before reading extension data.
