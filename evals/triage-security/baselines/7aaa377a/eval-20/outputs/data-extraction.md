# Step 1 -- Data Extraction

## Extracted CVE Data

Issue TC-8001 was fetched from Jira along with its remote links. The following
fields were parsed from the issue:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Status | New |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the
**2.2.x** version stream in the Version Streams table from Security Configuration.
Triage is scoped to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem
Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is
**Cargo**. Cargo is a source dependency ecosystem, which means remediation
will produce two tasks per stream: an upstream backport task and a downstream
propagation subtask (with the downstream blocked by the upstream task).

### Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository
`rhtpa-backend`. The Source Repositories table in the CLAUDE.md does not include
a Deployment Context column, so the deployment context defaults to `upstream`.
