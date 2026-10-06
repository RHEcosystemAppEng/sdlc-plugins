# Step 1 -- Data Extraction

## Issue: TC-8005

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
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (no comments) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream
(Konflux release repo: `rhtpa-release.0.4.z`).

## Ecosystem Detection

Vulnerable library **openssl-libs** is an RPM system package. The 2.2.x stream's
Ecosystem Mappings table includes:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Ecosystem classification**: System package (RPM) -- remediation produces
**1 task** per affected stream (Konflux release repo fix only; no upstream step).

## Deployment Context

The affected repository (`rhtpa-backend`) has deployment context: **upstream**
(default -- Deployment Context column absent from Source Repositories table).
