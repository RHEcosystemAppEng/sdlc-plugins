# Step 1 - Data Extraction for TC-8005

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
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| CVSS | 7.1 (High) |
| Existing comments | None |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `openssl-libs` is an RPM system package. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the configured ecosystems are:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | git show <tag>:Cargo.lock | release/0.4.z |
| RPM | -- | rpms.lock.yaml | git show <tag>:rpms.lock.yaml | -- |

`openssl-libs` is a system-level RPM package (not a Cargo crate). It matches the **RPM** ecosystem row in the Ecosystem Mappings table.

Ecosystem classification: **System package (RPM)** -- produces 1 remediation task per stream (Konflux release repo fix only). No upstream backport + downstream propagation flow.
