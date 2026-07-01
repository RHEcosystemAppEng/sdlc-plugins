# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Issue Key | TC-8005 |
| Summary | CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2] |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x only. Steps 2-8 will be scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is a system-level RPM package (not a Cargo crate or npm package). Consulting the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**RPM** is listed in the Ecosystem Mappings table. The detected ecosystem is **RPM**.

- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Upstream Branch: none (RPM system packages have no upstream source repo branch)

Since RPM is a system package ecosystem, remediation will follow the single-task path (Konflux release repo fix only), not the two-task upstream+downstream flow used for source dependency ecosystems.

## Deployment Context Lookup

The Source Repositories table in the project CLAUDE.md does **not** include a Deployment Context column. Per Step 0 backward compatibility rules, all repositories default to `upstream`. The Coordination Guidance subsection will be omitted from remediation task descriptions.
