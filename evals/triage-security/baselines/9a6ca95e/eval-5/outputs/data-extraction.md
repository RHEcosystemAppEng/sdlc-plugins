# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| CVSS | 7.1 (High) |
| Due date | 2026-08-15 |
| Existing comments | (no comments) |
| Ecosystem | RPM |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2]) |
| Deployment context | upstream (default -- repository not found in Source Repositories with explicit context) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is scoped to the 2.2.x stream only. Versions from other streams (e.g., 2.1.x) are analyzed for cross-stream impact (Step 8 Case B) but are not included in Affects Versions corrections for this issue.

## Ecosystem Detection

The vulnerable library `openssl-libs` is an RPM system package. The 2.2.x stream's Ecosystem Mappings table lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | rpms.lock.yaml | `git show <tag>:rpms.lock.yaml` | -- |

Lock file: `rpms.lock.yaml` is configured for the RPM ecosystem. The lock file is the source of truth for version determination.
