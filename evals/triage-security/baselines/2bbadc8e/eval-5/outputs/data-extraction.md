# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured
Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

Triage is **scoped to the 2.2.x stream**. Steps 3 and 8 apply only to versions
within this stream. Cross-stream impact on 2.1.x is reported via Case A (Step 8).

## Ecosystem Detection

The vulnerable package `openssl-libs` is an RPM system package. Per the 2.2.x
stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

- **Ecosystem**: RPM (system package)
- **Lock file**: `rpms.lock.yaml` (configured for the RPM ecosystem)
- **Check command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- **Remediation task count per stream**: 1 (Konflux release repo fix only)

## Deployment Context Lookup

The affected repository `rhtpa-backend` is found in Source Repositories. No
Deployment Context column is present in the mock configuration, so the default
`upstream` context applies.
