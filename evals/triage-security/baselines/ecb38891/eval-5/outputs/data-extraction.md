# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | < 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | _(none -- RPM system package, no upstream PR)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |
| CVSS | 7.1 (High) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` matches stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

Issue stream scope: **2.2.x only**

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is an RPM system package (not a Cargo crate or npm package). The 2.2.x stream's Ecosystem Mappings table in `security-matrix.md` lists the following ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

openssl-libs is a system-level RPM package. It matches the **RPM** ecosystem row.

Per the ecosystem classification table:

| Category | Ecosystems | Remediation tasks per stream |
|----------|------------|------------------------------|
| Source dependency | Cargo, npm | 2 -- upstream backport + downstream propagation |
| System package | RPM | 1 -- Konflux release repo fix only |

**Detected ecosystem: RPM (system package)**. This means remediation will produce a single task per affected stream, not the two-task upstream+downstream flow used for source dependency ecosystems.

## Deployment Context Lookup

The affected component label is `pscomponent:org/rhtpa-server`. The Source Repositories table in the project CLAUDE.md does not include a Deployment Context column. Per Step 0, when the Deployment Context column is absent, all repositories default to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions.
