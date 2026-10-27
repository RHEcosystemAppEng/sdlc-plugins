# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Stream scope | **2.2.x** (mapped from summary suffix `[rhtpa-2.2]` to Version Streams row `2.2.x`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Status | New |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none) |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream, which is served by the Konflux release repo `rhtpa-release.0.4.z`. Triage is scoped to this stream only.

## Ecosystem Detection

The vulnerable package `openssl-libs` is an RPM system package. The 2.2.x stream's Ecosystem Mappings table lists the RPM ecosystem with:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Classification: **System package** -- produces 1 remediation task per affected stream (Konflux release repo fix).

## Vulnerability Description

A buffer over-read vulnerability in openssl-libs during X.509 certificate chain verification. The `X509_verify_cert()` code path does not properly validate the length field of a Subject Alternative Name extension, allowing a remote attacker to craft a certificate that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.
