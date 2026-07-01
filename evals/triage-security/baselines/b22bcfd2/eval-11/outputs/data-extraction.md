# Step 1 -- Data Extraction

## Extracted CVE Data from TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 (< 1.42.0) |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream Fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE Record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due Date | 2026-08-15 |
| Existing Comments | None |
| Existing Issue Links | None |
| Assignee | Unassigned |

### Custom Fields

| Custom Field | Field ID | Value |
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** stream in the Version Streams table (Konflux release repo: `rhtpa-release.0.3.z`). Triage is scoped to the 2.1.x stream only.

### Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the library name and the component context (rhtpa-backend is a Rust backend service), the ecosystem is **Cargo**. This matches the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, which lists Cargo with lock file `Cargo.lock`.

As a Cargo (source dependency) ecosystem, remediation would typically follow the two-task pattern:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

However, Step 4.4 preemptive task reconciliation may alter this outcome (see reconciliation.md).

### Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be added to remediation task descriptions.
