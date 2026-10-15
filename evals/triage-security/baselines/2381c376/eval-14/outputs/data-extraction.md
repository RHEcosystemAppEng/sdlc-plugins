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
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is **scoped** to the 2.2.x stream only. Steps 3--8 apply only to versions within this stream.

## Ecosystem Detection

The vulnerable library is `openssl-libs`, an RPM system package. Per the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

- **Ecosystem**: RPM (system package)
- **Category**: System package -- produces **1 remediation task** per affected stream (Konflux release repo fix only)
- **Lock file**: `rpms.lock.yaml` (configured -- lock file is the source of truth)

## Deployment Context

The affected repository `rhtpa-backend` has deployment context: **upstream** (default, no explicit Deployment Context column present in Source Repositories table).
