# Step 1 -- Data Extraction

## CVE Data Table

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
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none in remote links) |
| Due date | 2026-08-15 |
| Existing comments | (no comments) |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

The suffix `rhtpa-2.2` maps to the `2.2.x` row in the Version Streams table from Security Configuration. Triage is scoped to this stream for Steps 3-8.

## Ecosystem Detection

Vulnerable library `openssl-libs` is a system-level RPM package, not a source-level dependency (Cargo/npm). The Ecosystem Mappings table for the 2.2.x stream lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Detected ecosystem: **RPM** (system package)
Lock file: `rpms.lock.yaml` (configured for this stream)

## Deployment Context

The component label `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` repository in Source Repositories. The Source Repositories table in Security Configuration does not include a Deployment Context column, so the deployment context defaults to `upstream`.
