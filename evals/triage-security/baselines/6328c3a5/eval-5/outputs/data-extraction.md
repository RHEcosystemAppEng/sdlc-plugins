# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

- Stream: 2.2.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

Triage is scoped to the 2.2.x stream. Steps 3 and 4 will apply only to versions within this stream. Cross-stream impact (2.1.x) will be assessed in Case A analysis.

## Ecosystem Detection

The vulnerable package `openssl-libs` is an RPM system package. The 2.2.x stream's Ecosystem Mappings table lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | rpms.lock.yaml | `git show <tag>:rpms.lock.yaml` | -- |

Classification: **System package** (RPM) -- remediation produces 1 task per affected stream (Konflux release repo fix only).
