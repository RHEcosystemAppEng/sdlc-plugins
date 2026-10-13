# Step 1 -- Data Extraction: TC-8050

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Ecosystem | Cargo |
| Affected version range | versions before 0.5.2 (< 0.5.2) |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | _(none)_ |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the
**2.2.x** stream in the Version Streams table from Security Configuration.
Triage is scoped to this stream -- Steps 3 and 8 apply only to 2.2.x versions.

## Ecosystem Detection

- **Library**: criterion (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation task count per stream**: 2 (upstream fix + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` has no Deployment Context column in the
Source Repositories table (backward compatibility). Defaulting to `upstream`.
