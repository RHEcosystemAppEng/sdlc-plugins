# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | N/A (no GitHub PR in remote links) |
| Advisory URL | [RHSA-2026:4021](https://access.redhat.com/errata/RHSA-2026:4021) |
| CVE record URL | [CVE-2026-40215](https://www.cve.org/CVERecord?id=CVE-2026-40215) |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is **scoped to the 2.2.x stream only**. Steps 3 and 4 will apply only to 2.2.x versions. Cross-stream impact on 2.1.x is handled via Case A.

## Ecosystem Detection

The vulnerable package is **openssl-libs**, which is a system-level RPM package. From the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | rpms.lock.yaml | `git show <tag>:rpms.lock.yaml \| grep 'openssl-libs'` | -- |

- **Ecosystem**: RPM (system package)
- **Category**: System package -- produces 1 remediation task per stream (Konflux release repo fix only)
- **Lock file**: rpms.lock.yaml
- **Upstream Branch**: N/A (RPM packages do not have an upstream source branch in this configuration)

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories with no Deployment Context column present. Defaulting to `upstream`.
